##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
##Program: Grid & child classes
##Author:Sebastian Villate
##Date: November 7th 2019
##Description: A module that allows for easy modular implementation of  Grid, Menu, LetterGrids and WordGrid objects to use in pygame projects. Can be used to generate
##coordinates for any graphical display that requires a grid, as well as generating Menus (Grids of buttons), LetterGrids(grids of letter labels) and WordGrids
##(grids of word labels).
##Input: Mouse clicks to find indices for clicked cells
##---------------------------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from Label import *
pygame.init()
GREEN=(0,255,0)
RED=(255,0,0)
WHITE=(0,0,0)
#==================================================================================GRID================================================================================
class grid(object): #Generates a grid of cells

    def __init__(self,rect,collums,rows,gap=0,visible=True):
        self.x=rect[0]
        self.y=rect[1]  
        self.height=rect[3]
        self.width=rect[2]
        self.rect=rect
        self.collums=collums
        self.rows=rows
        self.visible=visible
        self.gap=gap
        self.selectedslope=None
        self.totalcells=collums*rows
        self.rectlist=[]# List of coordinates (X,Y,Width,Height) for each cell
        self.cellwidth=(self.width-(self.gap*(self.collums+1)))/self.collums
        self.cellheight=(self.height-(self.gap*(self.rows+1)))/self.rows
        self.selectedcells=[]#Used to store cells user has selected
        xpos=self.x
        ypos=self.y
        for i in range(self.rows):
            ypos+=self.gap
            xpos=self.x
            for i in range(self.collums): #Generates the coordinates row by row, appending each set to self.rectlist
                xpos+=self.gap
                self.rectlist.append([xpos,ypos,self.cellwidth,self.cellheight])
                xpos+=self.cellwidth
            ypos+=self.cellheight

    def draw(self,screen): #Draws all the rects in rectlist, creating a grid
        if self.visible:
            pygame.draw.rect(screen,WHITE,self.rect,2)
            for rect in self.rectlist:        
                    pygame.draw.rect(screen,WHITE,rect,2)


    def Get_Indice(self):
        if self.visible:
            mp=pygame.mouse.get_pos()
            for i,cell in enumerate(self.rectlist): #Returns the indice of the cell the mouse is on
                if pygame.Rect(cell).collidepoint(mp):
                    return i

    def Get_Row(self,indice):
        if self.visible:
            return (indice//self.collums)+1 #Returns row of cell based on indice
        
                    
    def Get_Collum(self,indice):
        if self.visible:
            collum=indice%self.collums #Returns row of collum based on indice
            if collum==0:
                collum==self.collums
            return collum
                    

    def Is_Adjacent(self,rect1,rect2,returnslope=False):  #Determines if two indices are adjacent to each other on the grid,
        slope=None                                        #and determines type of adjacency using the indice of the two cells
        if rect1==rect2+1 or rect1==rect2-1:
            if self.Get_Row(rect1)==self.Get_Row(rect2):  #returnslope parameter determines if the cells adjacency type is returned by the function or not
                if self.selectedslope==None:
                    self.selectedslope="Horizontal"
                if returnslope==True:
                    return True,"Horizontal"
                return True
        elif rect1==rect2-self.collums or rect1==rect2+self.collums:
            if self.selectedslope==None:
                self.selectedslope="Vertical"
            if returnslope==True:
                return True,"Vertical"
            return True
        elif rect1==rect2-self.collums-1 or rect1==rect2+self.collums+1:
            if self.Get_Collum(rect1)==self.Get_Collum(rect2)-1 or self.Get_Collum(rect1)==self.Get_Collum(rect2)+1:#Only includes cells directly to the left or right
                if self.selectedslope==None:
                    self.selectedslope="Diagonaldown"
                if returnslope==True:
                    return True,"Diagonaldown"
                return True
        elif rect1==rect2+self.collums-1 or rect1==rect2-self.collums+1:
            if self.Get_Collum(rect1)==self.Get_Collum(rect2)-1 or self.Get_Collum(rect1)==self.Get_Collum(rect2)+1:#Only includes cells directly to the left or right
                if self.selectedslope==None:
                    self.selectedslope="Diagonalup"
                if returnslope==True:
                    return True,"Diagonalup"
                return True
        if returnslope==True:
            return False,None
        return False

    def In_Line(self,newcell): #Used to determine if a cell is inline with the rest of the cells selected
        sortedcelllist=sorted(self.selectedcells) #Creates a copy of the self.selectedcells list sorted by indice
        FirstCellAdj,FirstCellSlope=self.Is_Adjacent(sortedcelllist[0],newcell,True) #Checks adjacency to first cell and type of slope
        LastCellAdj,LastCellSlope=self.Is_Adjacent(sortedcelllist[-1],newcell,True) #Checks adjacency to last cell and type of slope
        if FirstCellAdj and FirstCellSlope==self.selectedslope or LastCellAdj and LastCellSlope==self.selectedslope: #If the type of slope with the new cell is the 
            return True                                                                                              #same as the already established slope, and the 
        else:                                                                                                        #cell is adjacent to the first or the last cell,
            return False                                                                                             #returns True

    def Highlight_Cells(self,screen):  #Highlights all the cells in the self.selectedcells list
        if self.visible:
            for cell in self.selectedcells:
                pygame.draw.rect(screen,RED,self.rectlist[cell],0) #Draws a red rectangle behind all the selected cells

    def Remove_Cell(self,unwantedcell):
        self.selectedcells.remove(unwantedcell)

    def All_Adjacent(self,cell): #Returns all the adjacent cells from a cell
        adjacentcells=[]
        start=(self.Get_Row(cell)-2)*self.collums #Starts at all the cells in the row above
        end=((self.Get_Row(cell)+1)*self.collums) #Ends at all the cells in the row below
        for cellindice in range(start,end):
            if cellindice>=0 and cellindice<=self.totalcells: #Only checks positive, in range indices 
                if self.Is_Adjacent(cell,cellindice): #Checks adjacency for every cell
                    adjacentcells.append(cellindice)
        return adjacentcells
    
    def Select_Cell(self,cell): #Adds cell to self.selectedcells if not already in self.selectedcells
        if cell not in self.selectedcells:
            self.selectedcells.append(cell)
        

#====================================================================================MENU==============================================================================
class Menu(grid): #Creates a grid of buttons for an simple menu
    def __init__(self,rect,collums,rows,buttonlist,gap=0,visible=True):
        grid.__init__(self,rect,collums,rows,gap,visible)
        self.buttonlist=buttonlist
        self.buttons=[]
        self.oldbutton=None#Used to store the cell the mouse was previously on 
        for i,button in enumerate(self.buttonlist):
             self.buttons.append(Button(self.rectlist[i],button))#Creates button object for every item in self.buttonlist, and passes each button its x and
                                                                 #y coordinates based on the rects generated by the grid class

             
    def draw(self,screen): #Draws grid of buttons
        if self.visible:
            for button in self.buttons: 
                button.draw(screen)

    def animate(self):  #Animates the buttons based on the mouse position 
        CurrentButton=self.Get_Indice() #Gets indice of the cell the mouse is currently on
        if CurrentButton!=None and CurrentButton<len(self.buttons):
            if CurrentButton!= self.oldbutton: #If the button has not already been animated,
                self.buttons[CurrentButton].animate() #Animates the button
                if self.oldbutton!=None:
                    self.buttons[self.oldbutton].reset()#Resets the old button the mouse was on
                self.oldbutton=CurrentButton #Sets the new old button to the button the mouse is currently on
        else:
            if self.oldbutton!=None:
                self.buttons[self.oldbutton].reset()#Resets the old button when the mouse is off 
                self.oldbutton=None
#==================================================================================WORD GRID===========================================================================
class WordGrid(grid): #Used to display a grid of words in labels 

    def __init__(self,rect,collums,rows,gap=0,visible=True):     
        grid.__init__(self,rect,collums,rows,gap,visible)
        self.labels=[]  #Stores the list of wordlabels yo display
        self.borderwidth=0


    def draw(self,screen): #Draws the labels on screen
        if self.visible:
            for label in self.labels:
                label.draw(screen)

    def Generate_Labels(self,letterlist):
        for i,letter in enumerate(letterlist):#Generates a label for every item in lettelist, determining the x and y based of the rectlist generated by grid()
            self.labels.append(Label(letter,self.rectlist[i],self.borderwidth))

#------------------------------------------------------------------------Letter Grid-----------------------------------------------------------------------------------
class LetterGrid(WordGrid):  #Used to generate a grid of letter labels used for  word search game
    def __init__(self,rect,collums,rows,gap=0,visible=True):
        WordGrid.__init__(self,rect,collums,rows,gap,visible)
        self.foundwords=[] #Stores a list of found words 
        self.borderwidth=1

    def Remove_Cells(self,unwantedcell): #Used to remove cells that are invalidated by a cell removal, assumes first cell selected is correct
        dellist=[] #List of cells to delete
        sortedcelllist=sorted(self.selectedcells) #Creates a copy of selected cells sorted by indice
        if unwantedcell>self.selectedcells[0]: #If the cell to remove is to the left of the first cell selected on the grid 
            for i in range (sortedcelllist.index(unwantedcell),len(sortedcelllist)):
                dellist.append(sortedcelllist[i]) #Appends all cells to the left of the cell to remove to dellist
            for cell in dellist:
                self.selectedcells.remove(cell)#Removes all the cells in dellist from self.selectedcells
        elif unwantedcell<self.selectedcells[0]: #If the unwanted cell is to the right of the first cell selected on the grid
            for i in range (sortedcelllist.index(unwantedcell)+1): 
                dellist.append(sortedcelllist[i]) #Appends all cells to the right of the unwantedcell to dellist
            for cell in dellist:
                self.selectedcells.remove(cell) #Removes all the cells in dellist from self.selectedcells
        elif unwantedcell==self.selectedcells[0]: #If the cell to remove is the first cell that was clicked
            self.selectedcells=[] #Clear the list of selected cells
            self.selectedslope=None
        if len(self.selectedcells)<=1: #Resets the slope of the selected cells list to none if the list is empty or only one cell 
            self.selectedslope=None    
                                        
    def Check_Words(self,puzzle,wordgrid):  #Checks if the cells in self.selectedcells spells a word             
        forwardsword=[]                         
        backwardsword=[]                        
        sortedcelllist=sorted(self.selectedcells) #Sorts the cell by indice to have them in the order on the grid regardless of how they were selected
        for indice in sortedcelllist:
            forwardsword.append(puzzle.letters[indice]) #Forwards word is the text object of all the cells 
        forwardsword=''.join(forwardsword) #Joins all the items in the list to create a string
        reversesortedcelllist=sorted(self.selectedcells,reverse=True)
        for indice in reversesortedcelllist:
            backwardsword.append(puzzle.letters[indice]) #Creates a word with all the cell texts backwards (check for backwards word in grid)
        backwardsword=''.join(backwardsword)
        if forwardsword in puzzle.words or backwardsword in puzzle.words:#If either forwardsword or backwardsword is in puzzle.words
            if forwardsword in puzzle.words: #Determines if its the forwardsword
                word=forwardsword
                indiceofword=puzzle.words.index(word) #Finds indice of word in puzzle.words
            elif backwardsword in puzzle.words: #Determines if its the backwardsword
                word=backwardsword
                indiceofword=puzzle.words.index(word) #Finds the indice of the word in puzzle.words
            wordgrid.labels[indiceofword].Set_Font_Colour(GREEN)#Sets the colour of the word label's text to Green to indicate its been found
            if word not in self.foundwords:
                self.foundwords.append(word)#Appends the word to self.foundwords if not already in list
            for indice in sortedcelllist:
                self.labels[indice].Set_Font_Colour(GREEN) #Sets all the words letters in the lettergrid to green to indicate its been found
            self.selectedcells=[] #Clears the selected cells 
            self.selectedslope=None #Resets the slope to none
            return True

    
    
        
        
                      
        
