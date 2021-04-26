from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
import datetime
from utils import SecondaryScreen
import yaml
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.lang import Builder
from functools import partial
from kivy.clock import Clock
import zbarcam

from main import clear_sound

# ##################################################
# # LievreScreen - Ecran de l'enigme Lievre & Tortue
# ##################################################
check = 0
t = 30


class LievreScreen(SecondaryScreen):
    already_pressed = False

    def my_callback(screen, dt):
        global t
        t -= 1
        screen.ids.timer.text = str(t)
        if t==0:
            screen.stop()
            if screen.ids.answer.text == "mot de passe : XXXXXXXX":
                print("succès")
                clear_sound()
            else:
                screen.ids.answer.text = "mot de passe : XXXXXXXX"

    def start(self):
        if not self.already_pressed:
            Clock.schedule_interval(self.my_callback, 1)
            self.ids.zbarcam2.start()
            self.already_pressed = True

    def stop(self):
        Clock.unschedule(self.my_callback)
        self.ids.zbarcam2.stop()
        self.already_pressed = False
    pass

    def set(self):
        global t
        if t == 0:
            t = 30
            self.start()
        else:
            self.start()