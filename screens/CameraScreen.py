from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from components.GestureControlPanel import GestureControlPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import cv2
import yaml

import webbrowser

from kivy.uix.image import Image

from components.CustomButton import CustomButton

class CameraScreen(Screen):
    
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
            
    fonts = paths['assets']['fonts']
    icons = paths['assets']['icons']

    Builder.load_file('kv/screens/CameraScreen.kv')

    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        self.bind(size = self.resize)
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def on_stop(self):
        self.ids['GCP'].on_stop()
        cv2.destroyAllWindows()
        
                
        