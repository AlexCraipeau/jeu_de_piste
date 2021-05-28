import os
import string
from collections import namedtuple
import random
from kivy.app import App
from kivy_garden.xcamera import XCamera
import PIL
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.audio import SoundLoader
from kivy.utils import platform

from main import search_log, add_log, update_clear_log, clear_enigme_map, \
    clear_enigme_2_laby, clear_enigme_3_analyse, clear_enigme_4_pigpen, \
    clear_enigme_5_cryptex, clear_enigme_6_lievre, clear_enigme_7_dessin, \
    init_enigme_6_lievre, show_cross, hide_cross

from utils import fix_android_image
import sqlite3 as sql

MODULE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
already_loaded = False


class ZBarDecoder:
    @classmethod
    def is_usable(cls):
        return False

    def validate_code_types(self, code_types):
        available_code_types = self.get_available_code_types()

        if not all(
            code_type in available_code_types
            for code_type in code_types
        ):
            raise ValueError(
                f'Invalid code types: {code_types}. '
                f'Available code types: {available_code_types}'
            )


class PyZBarDecoder(ZBarDecoder):
    @classmethod
    def is_usable(cls):
        try:
            from pyzbar import pyzbar
            cls.pyzbar = pyzbar
            return True

        except ImportError:
            return False

    def get_available_code_types(self):
        return set(self.pyzbar.ZBarSymbol.__members__.keys())

    def decode(self, image, code_types):
        self.validate_code_types(code_types)
        pyzbar_code_types = set(
            getattr(self.pyzbar.ZBarSymbol, code_type)
            for code_type in code_types
        )
        return [
            ZBarCam.Symbol(type=code.type, data=code.data)
            for code in self.pyzbar.decode(
                image,
                symbols=pyzbar_code_types,
            )
        ]


class ZBarLightDecoder(ZBarDecoder):
    @classmethod
    def is_usable(cls):
        try:
            import zbarlight
            cls.zbarlight = zbarlight
            return True

        except ImportError:
            return False

    def get_available_code_types(self):
        return set(self.zbarlight.Symbologies.keys())

    def decode(self, image, code_types):
        self.validate_code_types(code_types)
        zbarlight_code_types = set(
            code_type.lower()
            for code_type in code_types
        )
        codes = self.zbarlight.scan_codes(
            zbarlight_code_types,
            image
        )

        # zbarlight.scan_codes() returns None instead of []
        if not codes:
            return []

        return [
            ZBarCam.Symbol(type=None, data=code)
            for code in codes
        ]


class XZbarDecoder(ZBarDecoder):
    """Proxy-like that deals with all the implementations."""
    available_implementations = {
        'pyzbar': PyZBarDecoder,
        'zbarlight': ZBarLightDecoder,
    }
    zbar_decoder = None

    def __init__(self):
        # making it a singleton so it gets initialized once
        XZbarDecoder.zbar_decoder = (
            self.zbar_decoder or self._get_implementation())

    def _get_implementation(self):
        for name, implementation in self.available_implementations.items():
            if implementation.is_usable():
                zbar_decoder = implementation()
                Logger.info('ZBarCam: Using implementation %s', name)
                return zbar_decoder
        else:
            raise ImportError(
                'No zbar implementation available '
                f'(tried {", ".join(self.available_implementations.keys())})'
            )

    def get_available_code_types(self):
        return self.zbar_decoder.get_available_code_types()

    def decode(self, image, code_types):
        return self.zbar_decoder.decode(image, code_types)


class ZBarCam(AnchorLayout):
    """
    Widget that use the Camera and zbar to detect qrcode.
    When found, the `codes` will be updated.
    """

    resolution = ListProperty([640, 480])
    last_symbol = ""
    bullshit = StringProperty('????????')
    symbols = ListProperty([])
    Symbol = namedtuple('Symbol', ['type', 'data'])
    # checking all possible types by default
    code_types = ListProperty(XZbarDecoder().get_available_code_types())

    def __init__(self, **kwargs):
        # lazy loading the kv file rather than loading at module level,
        # that way the `XCamera` import doesn't happen too early
        global already_loaded

        if not already_loaded:
            Builder.load_file(os.path.join(MODULE_DIRECTORY, "zbarcam.kv"))
            self.already_loaded = True

        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self._setup())

    def _setup(self):
        """
        Postpones some setup tasks that require self.ids dictionary.
        """
        print("on passe par le setup")
        self._remove_shoot_button()
        # `self.xcamera._camera` instance may not be available if e.g.
        # the `CAMERA` permission is not granted
        self.xcamera.bind(on_camera_ready=self._on_camera_ready)
        # camera may still be ready before we bind the event
        if self.xcamera._camera is not None:
            self._on_camera_ready(self.xcamera)

    def _on_camera_ready(self, xcamera):
        """
        Starts binding when the `xcamera._camera` instance is ready.
        """
        xcamera._camera.bind(on_texture=self._on_texture)

    def _remove_shoot_button(self):
        """
        Removes the "shoot button", see:
        https://github.com/kivy-garden/garden.xcamera/pull/3
        """
        print("on remove le button")
        xcamera = self.xcamera
        shoot_button = xcamera.children[0]
        xcamera.remove_widget(shoot_button)

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
        pil_image = fix_android_image(pil_image)
        symbols = []
        codes = XZbarDecoder().decode(pil_image, code_types)
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

    @classmethod
    def random_gen(cls):
        print("JE PASSE PAR LA HIHIHI")
        cls.bullshit = ''.join(random.choice(string.ascii_letters) for x in range(8))
        print(App.get_running_app().root.get_screen("lievre").ids.answer)
        App.get_running_app().root.get_screen('lievre').ids.answer.text = "mot de passe : " + cls.bullshit
        print(cls.bullshit)
        return True

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

    @classmethod
    def check_password(cls, password):
        print("checking password")
        conn = sql.connect('jdp.db')
        cur = conn.cursor()
        cur.execute("""
        SELECT * FROM passwords
        WHERE password = ?
        LIMIT 1;""", [password])
        result = cur.fetchone()
        print("checkpassword result :", result)
        # Si un mot de passe correspond et que celui-ci n'a pas
        # encore été trouvé, débloque le mot de passe
        if result:
            if result[3] == 0:

                new_pass = SoundLoader.load('resources/sounds/new_pass.wav')

                new_pass.play()

                if result[2] != "":
                    exec(result[2], globals(), locals())
                else:
                    add_log(App.get_running_app().root, search_log(password))
                    update_clear_log(password)

                print(App.get_running_app())
                print(App.get_running_app().root)
                print(password)
                #add_log(App.get_running_app().root, search_log(password))
                conn.close()
            # c'est dégueu
            conn.close()
        conn.close()
        return True