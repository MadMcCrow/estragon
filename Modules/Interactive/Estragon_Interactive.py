from Question.Question_Menu import Menu

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonMenu(Menu)  :

    def __init__(self, MenuName):
        title = "Estragon"+ str(MenuName)
        super().__init__(title)
        self._MenuSize = 45

    
    class Submenus(Menu.Answer)  :
        def __init__(self, displayText):
            # ignore anwser init, we're gonna simplify it all
            object.__init__(self)
            self._Text = str(displayText)
    
    Texts = list()

    def makeDisplayTexts(self) :
        if len(self.Texts) > 0 :
            for t in self.Texts:
                ans = EstragonMenu.Submenus(t)
                self.addPossibleAnwser(ans)
        else :
            ans = EstragonMenu.Submenus("OK")
            self.addPossibleAnwser(ans)
    
    def __int__(self)   :
        return 



class StartInteractive(object)  :
    
        def __init__(self):
            super.__init(self)
            try :
                from Estragon_WelcomeMenu   import WelcomeMenu
                from Estragon_WelcomeMenu   import GoodbyeMenu
                from Estragon_MainMenu      import MainMenu
                # say hello
                WelcomeMenu()
                #say goodbye
                GoodbyeMenu()
            except NotImplementedError as err:
                print("the interactive mode is not working yet : ", err)
            finally:
                del self



        
