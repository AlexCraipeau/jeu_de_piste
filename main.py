from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import sqlite3 as sql
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
    def reinit_popup(self):
        popup = ReinitPopup(title='Réinitaliser ?',
                            size_hint=(None, None), size=(400, 200))
        popup.open()
        return True


##################################################
# QrcodeScreen - Ecran de récupération des qrcodes
##################################################
class QrcodeScreen(SecondaryScreen):
    pass


# ##################################################
# # SettingsScreen - Ecran des paramètres
# ##################################################
# class SettingsScreen(SecondaryScreen):
#     settings = SettingOptions()
#     settings.options = ["Réinitialiser le jeu"]
#     pass


##################################################
# PasslistScreen - Ecran de visionnage des mots de passe (temporaire)
##################################################
class PasslistScreen(SecondaryScreen):
    def show_pass(self):
        conn = sql.connect('jdp.db')
        cur = conn.cursor()
        cur.execute("""
               SELECT password FROM passwords
               WHERE unlocked = 1;""")
        result = cur.fetchall()
        pass_list = []
        for res in result:
            pass_list.append(res[0])
        conn.close()
        popup = Popup(title='Mots de passe trouvés',
                      content=Label(text='\n'.join(pass_list)),
                      size_hint=(None, None), size=(400, 400))
        popup.open()
    pass


##################################################
# ReinitPopup - Option de réinitialisation du jeu
##################################################
class ReinitPopup(Popup):
    text = StringProperty('Souhaitez-vous réinitialiser le jeu ?\n'
                          'ATTENTION, VOUS PERDREZ TOUT PROGRES.')

    ok_text = StringProperty('Réinitialiser')
    cancel_text = StringProperty('Annuler')

    __events__ = ('on_reinit', 'on_cancel')

    def ok(self):
        self.dispatch('on_reinit')
        self.dismiss()

    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()

    def on_reinit(self):
        # Ouverture de la connexion
        conn = sql.connect('jdp.db')
        cur = conn.cursor()

        # Passage à 0 de chaque champ unlocked
        cur.execute("""
        UPDATE passwords
        SET unlocked = 0;
        """)
        conn.commit()
        conn.close()
        return True

    def on_cancel(self):
        pass


##################################################
# JdpMain - Point d'entrée de l'application
##################################################
class JdpMain(App):
    def build(self):
        screen_manager.add_widget(JdpGrid(name='main'))
        screen_manager.add_widget(QrcodeScreen(name='qrcode'))
        screen_manager.add_widget(PasslistScreen(name='passlist'))
        return screen_manager

if __name__ == "__main__":
    JdpMain().run()
