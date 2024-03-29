############################################################
############################################################
import os
import string
from collections import namedtuple
import random

import PIL
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from PIL import ImageOps
from pyzbar import pyzbar
from kivy_garden.xcamera import XCamera
import sqlite3 as sql

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `codes` will be updated.
    """
    resolution = ListProperty([640, 480])
    last_symbol = ""
    symbols = ListProperty([])
    bullshit = StringProperty('XXXXXXXX')
    Symbol = namedtuple('Symbol', ['type', 'data'])
    # checking all possible types by default
    code_types = ListProperty(set(pyzbar.ZBarSymbol))

    pass_list = [] # A REMPLACER PAR UN FICHIER INDEPENDANT

    def __init__(self, **kwargs):
        self._request_android_permissions()
        # lazy loading the kv file rather than loading at module level,
        # that way the `XCamera` import doesn't happen too early
        Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))
        super(ZBarCam, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        self._remove_shoot_button()
        self._enable_android_autofocus()
        self.xcamera._camera.bind(on_texture=self._on_texture)
        # self.add_widget(self.xcamera)

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

    def _enable_android_autofocus(self):
        """
        Enables autofocus on Android.
        """
        if not self.is_android():
            return
        camera = self.xcamera._camera._android_camera
        params = camera.getParameters()
        params.setFocusMode('continuous-video')
        camera.setParameters(params)

    def _request_android_permissions(self):
        """
        Requests CAMERA permission on Android.
        """
        if not self.is_android():
            return
        from android.permissions import request_permission, Permission
        request_permission(Permission.CAMERA)

    @classmethod
    def _fix_android_image(cls, pil_image):
        """
        On Android, the image seems mirrored and rotated somehow, refs #32.
        """
        if not cls.is_android():
            return pil_image
        pil_image = pil_image.rotate(90)
        pil_image = ImageOps.mirror(pil_image)
        return pil_image

    def _on_texture(self, instance):
        self.symbols = self._detect_qrcode_frame(
            texture=instance.texture, code_types=self.code_types)

    @classmethod
    def _detect_qrcode_frame(cls, texture, code_types):
        dummy_list = ['nawak', 'hihihi', 'essaye_encore',
                      'mortdelol', 'fauxqr', 'qrcoude']
        image_data = texture.pixels
        size = texture.size
        # Fix for mode mismatch between texture.colorfmt and data returned by
        # texture.pixels. texture.pixels always returns RGBA, so that should
        # be passed to PIL no matter what texture.colorfmt returns. refs:
        # https://github.com/AndreMiras/garden.zbarcam/issues/41
        pil_image = PIL.Image.frombytes(mode='RGBA', size=size,
                                        data=image_data)
        pil_image = cls._fix_android_image(pil_image)
        symbols = []
        codes = pyzbar.decode(pil_image, symbols=code_types)
        for code in codes:
            symbol = ZBarCam.Symbol(type=code.type, data=code.data)
            symbols.append(symbol)
            print(str(symbol.data.decode("utf-8")))
            if cls.last_symbol != symbol.data:
                if str(symbol.data.decode("utf-8")) in dummy_list:
                    cls.random_gen()
                    print("rentrée dans random-gen")
                else:
                    cls.check_password(symbol.data.decode('utf-8'))
                cls.last_symbol = symbol.data

        return symbols

    @property
    def xcamera(self):
        return self.ids['xcamera']

    def start(self):
        self.xcamera.play = True

    def stop(self):
        self.xcamera.play = False

    @staticmethod
    def is_android():
        return platform == 'android'

    @staticmethod
    def is_ios():
        return platform == 'ios'

############################################################
# Méthodes ajoutées (détection/gestion de mots de passe)
############################################################

    @classmethod
    def check_password(cls, password):
        conn = sql.connect('jdp.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM passwords
        WHERE password = ?
        LIMIT 1;""", [password])
        result = cur.fetchone()
        # Si un mot de passe correspond et que celui-ci n'a pas
        # encore été trouvé, débloque le mot de passe
        if result:
            if result[2] == 0:

                new_pass = SoundLoader.load('resources/sounds/new_pass.wav')

                new_pass.play()
                cur.execute("""
                        UPDATE passwords
                        SET unlocked = 1
                        WHERE password = ?;""", [password])
                conn.commit()
        conn.close()

        return True

    @classmethod
    def random_gen(cls):
        print("JE PASSE PAR LA HIHIHI")
        cls.bullshit = ''.join(random.choice(string.ascii_letters) for x in range(8))
        print(App.get_running_app().root.get_screen("lievre").ids.answer)
        #App.get_running_app().root.get_screen('lievre').ids.answer.text = "mot de passe : " + cls.bullshit
        print(cls.bullshit)
        return True


