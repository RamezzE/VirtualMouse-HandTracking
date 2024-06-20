from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from views.components.CustomButton import CustomButton

from kivy.core.window import Window

from kivy.lang import Builder

from kivy.uix.screenmanager import Screen

class HomeScreen(Screen):
    
    Builder.load_file('kv/HomeScreen.kv')

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        
        self.bind(size = self.resize) 
    
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['home'].size = self.size
        
    def switch_to_camera_screen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'camera'