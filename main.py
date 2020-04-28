from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from zbarcam import *

# Objets globaux
screen_manager = ScreenManager() # Gestionnaire de changement d'écran


##################################################
# SecondaryScreen - Tout écran différent de la map
# Gère la touche BACK sur Android
##################################################
class SecondaryScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondaryScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)

    # Gestion de la touche BACK d'Android
    def android_back_click(self, window, key, *largs):
        if key == 27: # ESC (BACK sur Android)
            screen_manager.current = 'main'
            return True


##################################################
# JdpGrid - Ecran principal (map)
##################################################
class JdpGrid(Screen):
    pass


##################################################
# QrcodeScreen - Ecran de récupération des qrcodes
##################################################
class QrcodeScreen(SecondaryScreen):
    pass


##################################################
# JdpMain - Point d'entrée de l'application
##################################################
class JdpMain(App):
    def build(self):
        screen_manager.add_widget(JdpGrid(name='main'))
        screen_manager.add_widget(QrcodeScreen(name='qrcode'))
        return screen_manager


if __name__ == "__main__":
    JdpMain().run()
