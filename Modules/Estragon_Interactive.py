#import log
from .Estragon_Log import EstragonLog as Log


#Class to start launching 
class StartInteractive(object)  :
    
        def __init__(self):
            super().__init__()
            try :
                # get necessary classes
                from .Estragon_Menus.Estragon_WelcomeMenu import GoodbyeMenu
                from .Estragon_Menus.Estragon_WelcomeMenu import WelcomeMenu
                from .Estragon_Menus.Estragon_MainMenu    import MainMenu 
                # say hello
                WelcomeMenu()
                #start
                MainMenu()
                #say goodbye
                GoodbyeMenu()
            except NotImplementedError as err:
                print("the interactive mode is not working yet : ", err)
                raise
            finally:
                del self



        
