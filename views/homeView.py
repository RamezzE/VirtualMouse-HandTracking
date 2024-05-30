from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# import button

from components.CustomButton import CustomButton

import yaml

with open('paths.yaml', 'r') as f:
    paths = yaml.safe_load(f)
    
iconsPaths = paths['assets']['icons']
fontsPaths = paths['assets']['fonts']

class HomeScreen(Widget):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.root = FloatLayout()

        topBar = FloatLayout(size_hint=(1, 0.1), pos_hint={'top': 1, 'right' : 1})

        spacer = Widget(size_hint_x = 0.1)
        topBar.add_widget(spacer)

        settings_icon = Image(source=iconsPaths['settings'], size_hint=(None, 1), pos_hint={'right': 1, 'top': 0.9})
        topBar.add_widget(settings_icon)

        self.root.add_widget(topBar)

        title = Label(text='Virtual\nMouse', font_size = 64, size_hint=(1, 1), pos_hint = {'center_x' : 0.5, 'center_y' : 0.6} , font_name = fontsPaths['main_font'])
        self.root.add_widget(title)

        with self.root.canvas.before:
            Color(0.102, 0.027, 0.145, 1)
            self.rect = Rectangle(pos = self.root.pos, size = self.root.size)        
        
        getStartedButton = CustomButton(text='Get Started', size_hint=(0.5, 0.12), pos_hint={'center_x': 0.5, 'center_y': 0.3}, font_name = fontsPaths['main_font'], font_size = 40, default_color = [92/255, 41/255, 153/255, 1], pressed_color = [0.5, 0.5, 0.5, 1], text_color = [1, 1, 1, 0.75], border_radius = 20)
                
        self.root.add_widget(getStartedButton)
        
        pointer_icon = Image(source=iconsPaths['pointer'], size_hint=(0.1, 0.1), pos_hint={'center_x': 0.65, 'center_y': 0.24})

        self.root.add_widget(pointer_icon)
        self.root.bind(pos=self._updateBackground, size=self._updateBackground)

    def _updateBackground(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def getRoot(self):
        return self.root
