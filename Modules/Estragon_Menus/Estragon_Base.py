# Main Menu classes for estragon
from Question.Question_Menu     import Menu
from Question.Question_Prompt   import Prompt
from Estragon_Log import EstragonLog as Log

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
            Log("starting menu " + str(MenuName))
            self.Texts = self.ChoicesTextsFactory()
            title = "Estragon : "+ str(MenuName)
            super().__init__(title)
            self.makeDisplayTexts()
            self._MenuSize = 55
            self.ApplyChoices(self.getChoiceIdx())
        except NotImplementedError:
            pass

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonPrompt(Prompt)  :

    def initString(self)    :
        return str()

    def __init__(self, MenuName, initstr = None):
        title = "Estragon : "+ str(MenuName)
        super().__init__(title)
        if initstr is None:
            self._UserString = self.initString()
        elif isinstance(initstr, str)    :
            self._UserString = initstr
        self._MenuSize = 55
   
    def __str__(self)   :
        return self.gatherString()

    def recall(self)    :



