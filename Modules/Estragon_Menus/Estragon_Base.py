# Main Menu classes for estragon
from .Question.Question_Menu     import Menu
from .Question.Question_Prompt   import Prompt

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonMenu(Menu)  :
    
    class Submenus(Menu.Answer)  :
        def __init__(self, displayText):
            super().__init__()
            self._Text = str(displayText)
    
    Texts = list()

    class Test() :
        def getstr(self) :
            return str("OK" + str(self))

    def makeDisplayTexts(self) :
        self._PossibleAnwsers = list()
        if len(self.Texts) > 0 :
            for t in self.Texts:
                ans = Menu.Answer(EstragonMenu.Test())
                self._PossibleAnwsers.insert(ans)
        else :
            ans = Menu.Answer(EstragonMenu.Test())
            #ans = EstragonMenu.Submenus("OK" + str(self))
            self._PossibleAnwsers.insert(ans)
    
    def __int__(self)   :  
        return self.getSelectedIdx()

    def __init__(self, MenuName):
        title = "Estragon : "+ str(MenuName)
        super().__init__(title)
        self._MenuSize = 45
        self.ask()

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonPrompt(Prompt)  :

    def __init__(self, MenuName):
        title = "Estragon : "+ str(MenuName)
        super().__init__(title)
        self._MenuSize = 45
        self.ask()
   
    def __str__(self)   :
        return self.gatherString()


