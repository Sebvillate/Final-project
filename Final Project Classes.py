import Label

class Folder():

    def __init__(title,contents):
        self.title=title
        self.contents=contents
        
class Task():
    
    def __init__(self,title,code,description,duedate,priority,parentfolder):
        self.title=title
        self.taskcode=code
        self.description=description
        self.duedate=duedate
        self.priority=priority
        self.parentfolder=parentfolder
        
def generatefolders(folderfile):
    masterfolder=[]
    currentline=folderfile.readline().strip()
    if currentline=="}":
        return
    elif currentline=="{":
        masterfolder.append(Folder(currentline,generatefolders(folderfile)))
    generatefolder(folderfile)
        
        

    
class FileTools():

    def SaveTask(task,taskfile,folderfile):
        f=open(taskfile,'a')
        fi=open(folderfile,'r')
        f.write(str(task.taskcode)+"\n")
        f.write(str(task.title)+"\n")
        f.write(str(task.description)+"\n")
        f.write(str(task.duedate)+"\n")
        f.write(str(task.priority)+"\n")
        AllFileLines=fi.readlines()
        for line in AllFileLines:
            #print(line)
            print(line.join(e for e in line if e.isalpha()))
            if line.join(e for e in line if e.isalpha())==task.parentfolder:
                pass
        f.close()

    def ReadInFilePath(folderfile,taskfile):
        f=open(file,'r')
        fi=open(file,'r')
        
global fi=open(folderfile,'r')

print(generatefolder(fi))
##tasko=Task("Pee",1,"Banana","Dec 9",5,"School*Math")
##FileTools.SaveTask(tasko,"Saved Tasks.txt","Folder Folder.txt")
##        
##        
##        
##    
##
##    
##    
##
