from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from components.GestureControlPanel import GestureControlPanel
from components.CustomButton import CustomButton

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import cv2
import yaml

import webbrowser

from kivy.uix.image import Image

class CameraScreen(Screen):
        
    logsLabelText = ''
    
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
            
    fonts = paths['assets']['fonts']
    icons = paths['assets']['icons']
    
    isCameraRunning = None
    
    Builder.load_file('kv/screens/CameraScreen.kv')

    def __init__(self, **kwargs):
        super(CameraScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        
        self.isCameraRunning = False
        
        self.logs = []
        self.ids['GCP'].updateLog = self.updateLog
        
        self.bind(size = self.resize)        

    def startCamera(self):
        print('Starting camera')
        self.ids['GCP'].startCamera()
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def updateLog(self, message):
        self.logs.append(message)
        
        if len(self.logs) > 5:
            self.logs.pop(0)
            
        self.ids['logsLabel'].text = '\n'.join(self.logs)
        
    def openSettings(self):
        self.manager.transition.direction = 'up'
        self.manager.current = 'settings'
        self.on_stop()
        
    def openHome(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'
        self.on_stop()
        
    def on_stop(self):
        self.ids['GCP'].on_stop()
        cv2.destroyAllWindows()