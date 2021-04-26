from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.utils import platform
from PIL import ImageOps

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
        print(key)
        if key == 270:  # ESC (BACK sur Android) - anciennement 27
            App.get_running_app().root.current = 'main'
            return True


def is_android():
    return platform == 'android'


def is_ios():
    return platform == 'ios'


def fix_android_image(pil_image):
    """
    On Android, the image seems mirrored and rotated somehow, refs #32.
    """
    if not is_android():
        return pil_image
    pil_image = pil_image.rotate(90)
    pil_image = ImageOps.mirror(pil_image)
    return pil_image