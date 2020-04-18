# Main Menu classes for estragon

from .Estragon_Base import EstragonMenu

# Welcome menu class 
class WelcomeMenu(EstragonMenu)  :
    
    def __init__(self)  :
        super().__init__("Welcome to Estragon")


# Goodbye menu class 
class GoodbyeMenu(EstragonMenu)  :
    
    def __init__(self)  :
         super().__init__("Estragon will exit now")

