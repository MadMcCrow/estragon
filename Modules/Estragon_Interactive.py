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
                A = WelcomeMenu()
                B = WelcomeMenu()
                #start
                B = MainMenu()
                #say goodbye
                C = GoodbyeMenu()
            except NotImplementedError as err:
                Log("interactiveMode not implemented " + str(err))
            finally:
                del self



        
