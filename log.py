from kivy.properties import StringProperty

from utils import SecondaryScreen
import sqlite3 as sql
from kivy.uix.label import Label
import utils
from kivy.uix.scrollview import ScrollView

class LogContent(ScrollView):
    text = StringProperty('')
    #méthode "on_discovery(password)" à appeler à chaque unlock
    #Va chercher en bdd le texte correspondant
    #Ajoute au texte déjà présent selon un format défini (Titre - > contenu)

    pass

class LogScreen(SecondaryScreen):
    text = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    pass



