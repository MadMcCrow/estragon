# Main Menu classes for estragon
from Estragon_Log import EstragonLog as Log
from Estragon_Base import EstragonMenu

# Main menu class 
class MainMenu(EstragonMenu)  :
  
    def __init__(self)  :
        super().__init__("Main Menu")


    @staticmethod
    def DownloadEditor()    :
        try:
            from Estragon_GetEditorMenu import GetEditorMenu
            GetEditorMenu()
        except Exception    :
            Log("failed to use get Editor Menu")
            raise

    @staticmethod
    def InitLocalRepo()     :
        raise NotImplementedError

    @staticmethod
    def GDNative()          :
        raise NotImplementedError



    def ChoicesTextsFactory(self)  :
        A = "get Editor via github"
        B = "Use Already downloaded repository"
        C = "Setup godot project for GDNative"
        return [A,B,C]

    def ApplyChoices(self, idx)  :
        Log("idx is " + str(idx))
        assert self.isValidChoice()
        if idx == 0     :
            MainMenu.DownloadEditor()
        elif idx == 1   :
            MainMenu.InitLocalRepo()
        else            :
            MainMenu.GDNative()


 
    
        

