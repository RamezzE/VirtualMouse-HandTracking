from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
import yaml
from components.CustomButton import CustomButton

from kivy.core.window import Window

from kivy.lang import Builder

from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
            
    fonts = paths['assets']['fonts']
    
    size = Window.size
    pos = Window._pos
    
    Builder.load_file('kv/screens/HomeScreen.kv')

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        Window.bind(size=self.resize)
    
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['home'].size = self.size
        
    def toCameraScreen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'camera'