from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.base import EventLoop
from zbarcam import *
from kivy.properties import ObjectProperty

screen_manager = ScreenManager()


class SecondaryScreen(Screen):
    # Gestion de la touche BACK d'Android -> retour au main screen

    def __init__(self, **kwargs):
        super(SecondaryScreen, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key == 27:
            screen_manager.current = 'main'
            return True


class JdpGrid(Screen):
    pass


class QrcodeScreen(SecondaryScreen):
    pass


class JdpMain(App):
    def build(self):
        screen_manager.add_widget(JdpGrid(name='main'))
        screen_manager.add_widget(QrcodeScreen(name='qrcode'))
        return screen_manager


if __name__ == "__main__":
    JdpMain().run()
