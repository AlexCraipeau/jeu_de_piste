from utils import SecondaryScreen
import sqlite3 as sql
from kivy.uix.textinput import TextInput
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label


##################################################
# PasswordPopup - Rentrer un mot de passe
##################################################
class PasswordPopup(Popup):
#    text = StringProperty('Veuillez rentrer le mot de passe.')
    ok_text = StringProperty('Valider')
    cancel_text = StringProperty('Annuler')

    __events__ = ('on_press', 'on_cancel')

    def ok(self):
        self.dispatch('on_press')
        self.dismiss()

    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()

    def on_press(self):
        # Ouverture de la connexion
        conn = sql.connect('jdp.db')
        cur = conn.cursor()

        # Vérification matching mot de passe / bdd
        cur.execute("""
                 SELECT password from passwords
                 where password = '""" + self.ids.inp.text + """'
                 and unlocked = 0;""")
        result = cur.fetchall()

        # Si matching, débloquer mot de passe
        if result:
            new_pass = SoundLoader.load('resources/sounds/new_pass.wav')

            new_pass.play()
            cur.execute("""
            UPDATE passwords
            SET unlocked = 1
            WHERE password = ?;""", [self.ids.inp.text])
            conn.commit()
        conn.close()
        return True

    def on_cancel(self):
        pass


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

    def try_password(self):
        popup = PasswordPopup()
        popup.open()
    pass
