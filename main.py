### imports inutilisés
from kivy.app import App
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.clock import Clock
import sqlite3 as sql
# from kivy.uix.image import Image
# from kivy.uix.textinput import TextInput

### imports kivy
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix import dropdown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager

### imports généraux
import datetime

### imports internes
import enigmes
import fables
import password
import qrcodes
import utils
import log
from plyer import gps
from zbarcam import *

# Variables et fonctions globales (déso pas déso)
screen_manager = ScreenManager()  # Gestionnaire de changement d'écran
print("MAIN - CREATION DE LOGS LIST")
logs_list = []
first_pass = True
print(hex(id(logs_list)))

def show_pastille(screen_manager, enigme):
    screen_manager.get_screen('main').ids[enigme].disabled = False



def already_retrieved(enigme):
    conn = sql.connect('jdp.db')
    cur = conn.cursor()

    cur.execute("""
            SELECT password FROM passwords
            WHERE unlocked = 1 AND password = ? 
            ;""", [enigme])

    res = cur.fetchall()
    print("résultat already retrieved : " + str(res))
    conn.close()
    if res:
        print("enigme déjà cleared : " + str(enigme))
        return True
    else:
        print("nouvelle enigme cleared : " + str(enigme))
        return False

def retrieve_logs(screen_manager):
    conn = sql.connect('jdp.db')
    cur = conn.cursor()

    cur.execute("""
            SELECT password FROM passwords
            WHERE unlocked = 1
            ;""")

    res = cur.fetchall()
    print(res)
    for password in res:
        print("retrieve_logs - adding log : " + str(password[0]))
        add_log(screen_manager, search_log(password[0]))
    # fix dégueulasse pour régler le probleme de duplication
    # d'instanciation de la liste au démarrage
    global first_pass
    first_pass = True
    conn.close()

def add_log(screen_manager, lst):
    global logs_list
    global first_pass
    if logs_list == [] and first_pass:
        # fix dégueulasse pour régler le probleme de duplication
        # d'instanciation de la liste au démarrage
        first_pass = False
        retrieve_logs(screen_manager)
    # suite du fix dégueulasse : empêcher la duplication des logs :


    # print(hex(id(logs_list)))

    print("add_log - liste originale : " + str(logs_list))
    print('add_log - adding log : ',lst)
    # suite du fix dégueulasse : empêcher la duplication des logs :
    if lst not in logs_list:
        logs_list.append(lst)
        print("add_log - nouvelle liste des logs : " + str(logs_list))
        logs_list.sort(key=lambda x: x[1])
        print(logs_list)
        screen_manager.get_screen('log').ids['logs'].text = ''.join(str(elt[1]) + ' >> '+ str(elt[0]) + '\n_____________________________________________\n' for elt in logs_list)


def update_clear_log(log):
    conn = sql.connect('jdp.db')
    cur = conn.cursor()
    print("update_clear_log - rajout du log : " + str(log))
    # enigme_map débloquée en bdd
    cur.execute("""
    UPDATE passwords
    SET unlocked = 1
    WHERE password = ?;
    """, [log])
    conn.commit()
    conn.close()


def update_clear_enigme(enigme):
    conn = sql.connect('jdp.db')
    cur = conn.cursor()
    print("update_clear_enigme - déblocage de l'énigme : " + str(enigme))
    # enigme_map débloquée en bdd
    cur.execute("""
    UPDATE enigmes
    SET cleared = 1
    WHERE name = ?;
    """, [enigme])
    conn.commit()
    conn.close()

def clear_enigme_map(screen_manager):
    print(screen_manager.children)
    print("clear_enigme_map - passage dans clear_enigme_map")
    button_list = screen_manager.get_screen('main').ids.copy()
    button_list.pop('map')
    # Désactiver les boutons
    for id in button_list:
        screen_manager.get_screen('main').ids[id].disabled = True
        screen_manager.get_screen('main').ids[id].color = (0, 0, 0, 0)
    # Changer l'image
    screen_manager.get_screen('main').ids['map'].source = './resources/images/map_cleared.png'
    # Ajouter texte log
    show_pastille(screen_manager, "enigme_1")
    show_pastille(screen_manager, "enigme_2")
    screen_manager.get_screen('main').ids['qrcodebutton'].disabled = False

    #flag unlocked si pas déjà fait + ajout du log
    if not already_retrieved("enigme_map"):
        print("clear_enigme_map - premier déblocage d'engime_map")
        print("clear_enigme_map - rajout bouton logs")
        add_log(screen_manager, search_log('enigme_map'))
        update_clear_log('enigme_map')
        update_clear_enigme("enigme_map")


def clear_enigme_2_laby(screen_manager):
    show_pastille(screen_manager, "enigme_3")
    if not already_retrieved("log_3"):
        add_log(screen_manager, search_log("log_3"))
        add_log(screen_manager, search_log("log_4"))
        update_clear_log("log_3")
        update_clear_log("log_4")
        update_clear_enigme("enigme_2")
    print("clear enigme 2")


def clear_enigme_3_analyse(screen_manager):
    show_pastille(screen_manager, "enigme_4")
    add_log(screen_manager, search_log("log_5"))
    update_clear_log("log_5")
    update_clear_enigme("enigme_3")
    print("clear_enigme_3")

# changer log enigme pigpen pour password
def clear_enigme_4_pigpen(screen_manager):
    show_pastille(screen_manager, "enigme_5")
    add_log(screen_manager, search_log("log_8"))
    update_clear_log("log_8")
    add_log(screen_manager, search_log("log_8b"))
    update_clear_log("log_8b")

    update_clear_enigme("enigme_4")

    print("clear_enigme_4")


def clear_enigme_5_cryptex(screen_manager):
    print("clear_enigme_5_cryptex - passage")
    show_pastille(screen_manager, "enigme_6")
    add_log(screen_manager, search_log("log_9"))
    update_clear_log("log_9")
    #Ajouter timer invisible de 3 min qui déclenche log 9b
    add_log(screen_manager, search_log("log_9b"))
    update_clear_log("log_9b")
    update_clear_enigme("enigme_5")


def init_enigme_6_lievre(screen_manager):
    add_log(screen_manager, search_log("log_10"))
    update_clear_log("log_10")
    screen_manager.get_screen('main').ids['lievrebutton'].disabled = False

def clear_enigme_6_lievre(screen_manager):
    show_pastille(screen_manager, "enigme_7")
    add_log(screen_manager, search_log("log_11"))
    update_clear_log("log_11")
    update_clear_enigme("enigme_6")
    print("clear_enigme_6")


def clear_enigme_7_dessin(screen_manager):
    print("clear_enigme_7")
    add_log(screen_manager, search_log("log_13"))
    update_clear_log("log_13")
    update_clear_enigme("enigme_7")

# changer log enigme arcenciel pour password

def search_log(enigme):
    conn = sql.connect('jdp.db')
    cur = conn.cursor()

    cur.execute("""
    SELECT texte, position FROM textes
    WHERE password = '""" + str(enigme) + """'
     ORDER BY position;
    """)

    res = cur.fetchall()
    conn.close()

    print(res[0])
    return res[0]


# Lancement des fonctions d'avancement
def get_cleared_enigmes():
    conn = sql.connect('jdp.db')
    cur = conn.cursor()

    # Récupération de toutes les enigmes  cleared en bdd
    cur.execute("""
    SELECT * FROM enigmes
    WHERE cleared = 1;
    """)
    result = cur.fetchall()
    print("get_cleared_enigmes - enigmes à récupérer : " + str(result))
    for res in result:
        # execution de la fonction correspondante
        print("get_cleared_enigmes - executing : " + str(res[2]))
        exec(res[2], globals(), locals())

    conn.close()

def clear_sound():
    SoundLoader.load('resources/sounds/new_pass.wav').play()


def set_timer():
    # récupération du temps
    conn = sql.connect('jdp.db')
    cur = conn.cursor()
    print("passage dans set-timer")
    # Passage à 0 de chaque champ unlocked
    cur.execute("""SELECT * FROM time;""")
    t = cur.fetchone()
    print(t)
    if t:
        t = datetime.datetime.strptime(t[0], "%Y-%b-%d %H:%M:%S.%f")
    else:
        t = datetime.datetime.now()
        cur.execute("""INSERT INTO time VALUES
        (?);""", [t.strftime("%Y-%b-%d %H:%M:%S.%f")])
        conn.commit()

    conn.close()
    return t


# Set timer
original_time = set_timer()


class Time(Label):
    def update_time(self, *args):
        global original_time
        chrono = datetime.datetime.now() - original_time
        days, seconds = chrono.days, chrono.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        self.text = f"{hours}h{minutes:02}m{seconds:02}s"


class ChooseLocPopup(Popup):
    ok_text = StringProperty('Valider')
    cancel_text = StringProperty('Annuler')
    bttnid = StringProperty()
    text = StringProperty()
    curr_bttn_name = StringProperty()
    og_bttnid = StringProperty()
    __events__ = ('on_press', 'on_cancel')

    def open(self, id_name, name, **kwargs):
        super(ChooseLocPopup, self).open(**kwargs)
        self.curr_bttn_name = name
        self.ogbttnid = name

    def check_status(self, text):
        menu_buttons_list = ['qrcodebutton','lievrebutton', 'dessinbutton']
        button_list = App.get_running_app().root.get_screen('main').ids.copy()
        button_list.pop('map')
        for i in range(1,8):
            button_list.pop('enigme_'+str(i))
        for b in menu_buttons_list:
            button_list.pop(b)
        button_list[self.ogbttnid].text = text
        if self.curr_bttn_name == text:
            all_clear = True
            for id in button_list:
                if id != button_list[id].text:
                    all_clear = False
            if all_clear:
                clear_enigme_map(App.get_running_app().root)
               # Ajouter backlog ici ?
                clear_sound()

    def ok(self):
        self.dispatch('on_press')
        self.dismiss()

    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()

    def on_press(self):
        pass

    def on_cancel(self):
        pass


##################################################
# PopupBttn - Bouton de popup pour enigme 0
##################################################
class PopupBttn(Button):
    def open_popup(self):
        print(self.name)
        ChooseLocPopup().open(self.text, self.name)


##################################################
# JdpGrid - Ecran principal (map)
##################################################


class JdpGrid(Screen):
    t = Time()
    Clock.schedule_interval(t.update_time, 1)

    popup_text = StringProperty()

    def reinit_popup(self):
        popup = ReinitPopup(title='Réinitaliser ?',
                            size_hint=(None, None), size=(800, 400))
        popup.open()
        return True


# ##################################################
# # SettingsScreen - Ecran des paramètres
# ##################################################
# class SettingsScreen(SecondaryScreen):
#     settings = SettingOptions()
#     settings.options = ["Réinitialiser le jeu"]
#     pass


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
        global original_time
        # Ouverture de la connexion
        conn = sql.connect('jdp.db')
        cur = conn.cursor()

        # Passage à 0 de chaque champ unlocked
        cur.execute("""
        UPDATE passwords
        SET unlocked = 0;
        """)
        conn.commit()

        cur.execute("""
        UPDATE enigmes
        SET cleared = 0;
        """)
        conn.commit()

        # Retour au timer à 0
        cur.execute("""DELETE FROM time;""")
        conn.commit()
        original_time = set_timer()

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
        screen_manager.add_widget(qrcodes.QrcodeScreen(name='qrcode'))
        screen_manager.add_widget(password.PasslistScreen(name='pass'))
        screen_manager.add_widget(log.LogScreen(name='log'))
        # On enlève le screen des fables : inutile pour l'instant
        # screen_manager.add_widget(fables.FablesScreen(name='fables'))
        screen_manager.add_widget(enigmes.LievreScreen(name='lievre'))
        screen_manager.add_widget(enigmes.DessinScreen(name='dessin'))
        retrieve_logs(screen_manager)
        get_cleared_enigmes()
        # print(screen_manager.screen_names)
        return screen_manager


if __name__ == "__main__":
    JdpMain().run()