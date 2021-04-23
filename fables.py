from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from utils import SecondaryScreen
import yaml
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.lang import Builder


class FableButton(Button):
    content = ''

    def __init__(self, content,**kwargs):
        super().__init__(**kwargs)
        self.content = content
        pass

    def open_fable(self):
        pop = Popup(title=self.text, content=Label(text=self.content))
        pop.open()
        pass


class FablesScreen(SecondaryScreen):
    @mainthread
    def on_enter(self):
        with open('./resources/texts/fables.yaml') as file:
            fables_list = yaml.load(file, Loader=yaml.FullLoader)

            for fable in fables_list['fables']:
                self.ids.grid.add_widget(FableButton(content=fable['contenu'],text=fable['titre']))

    pass

