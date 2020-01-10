##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##Program: Labels and buttons
##Author:Sebastian Villate
##Date: November 7th 2019
##Description: A module that allows for easy, modular implementation of labels (Generated text objects) and Buttons(Inherits from label and gives button funtionality
##to a generated text object). Includes variety of methods to customize label colour, text, and alignment allowing for easy creation of graphically displayed text in
##pygame projects. Button class allows for the creation of a label, offering the same level of graphic customization, but gives the label button functionality to
##determine if the label has been clicked.
##Input: Mouse clicks to determine button presses and mouse position to determine button animations
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
pygame.init()
BLACK=(0,0,0)
#===================================================================================Label==============================================================================
class Label(object):
    def __init__(self,text,rect, border=0,xalignment="center",yalignment="center",fontstyle="Helvetica",dynamic=False,bordercolour=(255,255,255),textcolour=(255,255,255),fontsize=None,Bigfontsize=None,visible=True):
        self.rect=rect 
        self.xpos=rect[0]
        self.ypos=rect[1]
        self.width=rect[2]    
        self.height=rect[3] 
        self.text=text
        self.visible=True #Determines wether or not the Label is currently being displayed, also effects a buttons functionality
        self.fontstyle=fontstyle
        self.xalignment=xalignment  #Stores the x axis alignment for the text in the label (Left, Center, Right)
        self.yalignment=yalignment  #Stores the y axis alignment for the text in the label (Top, Center, Bottom)
        self.bordercolour=bordercolour        
        self.textcolour=textcolour
        self.Generate_Text(fontsize) #Generates the text object that is displayed in the label              
        self.dynamic=dynamic         # If True, creates a bigger text object to make the label's text size dynamic (Buttons animations or animated text)
        if self.dynamic:
            self.Generate_Large_Text(Bigfontsize)#Generates the larger font if the label is dynamic
        self.borderwidth=border
        self.currenttext=self.renderedtext #Sets by default to the small rendered text
        self.currenttextx=self.textx #Set by default to the smaller text's X coordinate
        self.currenttexty=self.texty #Set by default to the smaller text's Y coordinate

    def Generate_Text(self,fontsize):
        if fontsize==None: 
            fontsize=1
            while True:
                currentfont=pygame.font.SysFont(self.fontstyle,fontsize)        #If the fontsize it's passed ==None, runs a loop scaling the text up by one every time,
                text=currentfont.render(self.text,True,self.textcolour)         #until the rendered text's size is 80% of the labels size, generating a text that fills 
                textsize=[text.get_width(),text.get_height()]                   #the label perfectly every time
                if textsize[0]<=self.width*0.8 and textsize[1]<=self.height*0.8:
                    fontsize+=1
                else:
                    break
        self.fontsize=fontsize #If it is passed a specific fontsize, skips loop and renders everything based on the passed fontsize
        self.font=pygame.font.SysFont(self.fontstyle,fontsize) 
        self.renderedtext=self.font.render(self.text,True,self.textcolour)              
        self.textx,self.texty=self.Allign_Text(self.renderedtext) #Generates the x and y for the text to allign it in the label

    def Generate_Large_Text(self,fontsize):  # Does the same thing as Generate_Text(), but scales it to 95% of the label size to create a bigger font 
        fontsize=1                           # for dynamic labels.
        while True:
            currentfont=pygame.font.SysFont(self.fontstyle,fontsize)
            text=currentfont.render(self.text,True,self.textcolour)
            textsize=[text.get_width(),text.get_height()]
            if textsize[0]<=self.width*0.95 and textsize[1]<=self.height*0.95:
                fontsize+=1
            else:
                break
            self.bigfontsize=fontsize
            self.bigrenderedtext=text
            self.bigfont=currentfont                
            self.bigtextx,self.bigtexty=self.Allign_Text(self.bigrenderedtext)

    def Allign_Text(self,text):  #Aligns a generated text object based on the self.xalignment & self.yalignment attributes
        textsize=[text.get_width(),text.get_height()]
        if self.xalignment.lower()=="center":           #Sets the x coordinate of the text based on the horizontal alignment with the label
            textx=self.xpos+((self.width-textsize[0])/2)
        elif self.xalignment.lower()=="left":
            textx=self.xpos                                                     
        elif self.xalignment.lower()=="right":
            textx=self.xpos+(self.width-textsize[0])            
        if self.yalignment.lower()=="center":            #Sets the y coordinate of the text based on the vertical alignmnet with the Label
            texty=self.ypos+((self.height-textsize[1])/2)
        elif self.yalignment.lower()=="top":
            texty=self.ypos                                                         
        elif self.yalignment.lower()=="bottom":
            texty=self.ypos+(self.height-textsize[1])
        return textx,texty

        
            
        
        
    def draw(self,screen):      #Draws Label object 
        if self.visible:
            if self.borderwidth>0:
                pygame.draw.rect(screen,self.bordercolour,self.rect,self.borderwidth) #Draws a border for the label if self.borderwidth is >0
            screen.blit(self.currenttext,[self.currenttextx,self.currenttexty]) #blits the text within the Label

    def Set_Font_Colour(self,colour):   #Used to set the labels font colour
        self.textcolour=colour
        self.font=pygame.font.SysFont(self.fontstyle,self.fontsize) #Generates a new font and text with the updated colour
        self.renderedtext=self.font.render(self.text,True,self.textcolour)
        if self.dynamic:
            self.bigfont=pygame.font.SysFont(self.fontstyle,self.bigfontsize) #Generates a new big font with the updated text and colour if the label is dynamic
            self.bigrenderedtext=self.bigfont.render(self.text,True,self.textcolour)
        self.currenttext=self.renderedtext
        
    def Set_Font(self,font,size=None): #Sets the size and font of the default font and generates a new self.renderedtext with the updated font and size 
        self.fontstyle=font
        self.fontsize=size
        self.Generate_Text(self,self.fontsize)
        self.currenttext=self.renderedtext

    def Set_Big_Font(self,font,size=None): #If the label is dynamic, sets the size and font of the big text
        if self.dynamic:                   #object and generates a new self.bigrenderedtext with updated font and size
            self.fontstyle=font
            self.bigfontsize=size
            self.Generate_Large_Text(self,self.bigfontsize)
            self.currenttext=self.bigrenderedtext

    def Set_Border_Colour(self,colour):
        self.bordercolour=colour

    def Set_Border_Width(self,width):
        self.borderwidth=width

    def animate(self):
        if self.dynamic:
            self.currenttext=self.bigrenderedtext #Switches the label from the small font to the large font if the label is dynamic, animating the label 
            self.currenttextx=self.bigtextx       #and keeping the text alligned     
            self.currenttexty=self.bigtexty

    def reset(self):
        if self.dynamic:                         #Resets the label to the smaller font to reset it from its animated state
            self.currenttext=self.renderedtext
            self.currenttextx=self.textx
            self.currenttexty=self.texty
            
        
#==================================================================================Button===============================================================================
class Button(Label):
    

    
    def __init__(self,rect,text,border=1,xalignment="center",dynamic=True):
        Label.__init__(self,text,rect,border=border,xalignment=xalignment,dynamic=dynamic) #Graphical component for the button generated by Label()
        self.colour=BLACK #Background colour for button
                    
    def draw(self,screen):
        if self.visible: #Only draws button if it is visible
            if self.colour:
                pygame.draw.rect(screen,self.colour,self.rect,0) #Draws a backgroud colour for the button if there is one
            super().draw(screen) #Draws graphical component using Label() draw method.

    def Set_Colour(self,colour):
        self.colour=colour


    def Detect_Mouse(self): #Detects if the button has been clicked, giving the Label it's button functionality. Returns Boolean value
        if self.visible:
            if pygame.Rect(self.rect).collidepoint(pygame.mouse.get_pos()):
                return True
            else:
                return False
