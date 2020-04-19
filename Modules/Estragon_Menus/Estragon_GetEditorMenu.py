# Estragon class for displaying option for getting the editor

from Estragon_Base import EstragonMenu, EstragonPrompt
from Estragon_MainMenu import MainMenu


# main class for the get editor path
class GetEditorMenu(EstragonMenu)  :
  
    # the path we'll be using
    Path = str()

    # branch to use
    Branch = str()

    # url to use
    Url = str()

    def __init__(self)  :
        from os import path
        from os import getcwd
        self.Path = path.dirname(path.join(getcwd()))
        self.Url = "https://github.com/godotengine/godot.git"
        self.Branch = "master"
        super().__init__("Get Editor Menu")



    def ChangePath(self)    :
        newPrompt = EstragonPrompt("Path", self.Path )
        newPath = newPrompt.gatherString()
        from os.path import isdir
        if isdir(newPath)   :
            self.Path = newPath


    def ChangeUrl(self)     :
        newUrl = str(EstragonPrompt("Url", self.Url ))
        self.Url = newUrl

    
    def ChangeBranch(self)          :
        newBranch = str(EstragonPrompt("Branch", self.Branch ))
        self.Branch = newBranch


    def validate(self)  :
        raise NotImplementedError

    def ChoicesTextsFactory(self)  :
        A = "local path to use :\n" + str(self.Path)
        B = "distant git url to use :\n" + str(self.Url)
        C = "git branch to use:\n                                               \n" + str(self.Branch)
        D = "Validate"
        E = "Back"
        return [A,B,C,D,E]

    def ApplyChoices(self, idx)  :
        print(idx)
        #assert idx in range(0,len(self.ChoicesTextsFactory()))
        if idx == 0     :
            self.ChangePath()
            self.ask()
        elif idx == 1   :
            self.ChangeUrl()
            self.ask()
        elif idx == 2  :
            self.ChangeBranch()
            self.ask()
        elif idx == 3 :
            self.validate()
        else    :
            # go back to main menu
            MainMenu()
            
