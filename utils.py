from kivy.uix.screenmanager import Screen
from kivy.core.window import Window


##################################################
# SecondaryScreen - Tout écran différent de la map
# Gère la touche BACK sur Android
##################################################
class SecondaryScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondaryScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)

    # Gestion de la touche BACK d'Android
    @staticmethod
    def android_back_click(self, window, key, *largs):
        if key == 27:  # ESC (BACK sur Android)
            screen_manager.current = 'main'
            return True
