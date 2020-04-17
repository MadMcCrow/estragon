# Main Menu classes for estragon
from .Question.Question_Menu     import Menu
from .Question.Question_Prompt   import Prompt

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonMenu(Menu)  :
    
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
        return self.getSelectedIdx()

    def __init__(self, MenuName):
        title = "Estragon : "+ str(MenuName)
        super().__init__(title)
        self._MenuSize = 45
        self.makeDisplayTexts()
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


