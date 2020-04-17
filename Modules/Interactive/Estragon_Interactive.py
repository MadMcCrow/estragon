from Question.Question_Menu import Menu

# Main class for describing a menu
# implements Estragon Specific feature to overload Question features
class EstragonMenu(Menu)  :

    def __init__(self, MenuName):
        title = "Estragon"+ str(MenuName)
        super().__init__(title)
        self._MenuSize = 45