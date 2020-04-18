# Main Menu classes for estragon
from .Question.Question_Menu     import Menu
from .Question.Question_Prompt   import Prompt

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonMenu(Menu)  :
    
    Texts = list()

    def ChoicesTextsFactory(self)  :
        return ["ok"]

    def ApplyChoices(self, idx)  :
        raise NotImplementedError

    def makeDisplayTexts(self) :
        assert len(self.Texts) > 0
        self.setAvailableAnswers(self.Texts)
    
    def __int__(self)   :  
        return self.getSelectedIdx()

    def __init__(self, MenuName):
        try :
            self.Texts = self.ChoicesTextsFactory()
            title = "Estragon : "+ str(MenuName)
            super().__init__(title)
            self.makeDisplayTexts()
            self._MenuSize = 45
            self.ask()
            self.ApplyChoices(self.getChoiceIdx())
        except NotImplementedError:
            pass

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


