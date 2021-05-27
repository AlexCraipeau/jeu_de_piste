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
from kivy_garden.mapview import MapView
from functools import partial
from kivy.clock import Clock
import zbarcam
from plyer import gps

from main import clear_sound, clear_enigme_6_lievre, add_log, search_log

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
                clear_enigme_6_lievre(App.get_running_app().root)
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


class DessinScreen(SecondaryScreen):

    next_location = 1
    next_lat = 48.84208
    next_lon = 2.388240
# au besoin : https://stackoverflow.com/questions/40829408/how-to-trace-a-path-in-kivy-map
# pour dessiner direct sur la carte
# https://kivy-garden.github.io/mapview/mapview.html
# https://www.youtube.com/watch?v=P940dd1VxsU

    def on_gps_location(self, **kwargs):

        def get_next_loc_coordinates(self):
            return self.ids['point_' + str(self.next_location)].lat, self.ids['point_' + str(self.next_location)].lon
            # print(kwargs)

        self.ids['player'].lon = str(kwargs['lon'])
        self.ids['player'].lat = str(kwargs['lat'])

        self.ids['lat'].text = str(kwargs['lat'])
        self.ids['lon'].text = str(kwargs['lon'])
        self.ids['map'].center_on((kwargs['lat'],kwargs['lon']))

        if (self.ids['centerbutton'].disabled == False
                and self.ids['player'].lat > self.next_lat-0.00001
                and self.ids['player'].lat < self.next_lat+ 0.00001
                and self.ids['player'].lon > self.next_lon-0.00001
                and self.ids['player'].lat < self.next_lon + 0.00001):
            print(" Dessin - point trouvé !")
            #changement de couleur point actuel (complété)
            self.ids['point_' + str(self.next_location)].source = "./resources/images/gpsmarker.png"

            if self.next_location < 7:
                # changement du next_location
                self.next_location = self.next_location + 1
                # changement des next_lat/next_long
                self.next_lat, self.next_long = get_next_loc_coordinates()
                # affichage du point suivant
                self.ids['point_' + str(self.next_location)].source = "./resources/images/gpsmarker_next.png"
            elif self.location == 7:
                add_log(App.get_running_app().root, search_log("log_12"))
                self.next_lat = 10
                self.next_long = 10
                self.next_location = 8
                #evite de charger l'image en boucle - solution de merde
            else:
                print("Dessin - fini")



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        gps.configure(on_location=self.on_gps_location)
        print("On l'a créé hihihihihihi")
        gps.start()

