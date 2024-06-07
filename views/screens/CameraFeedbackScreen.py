from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from views.components.GestureDetectionView import GestureDetectionView 
from views.components.CustomButton import CustomButton

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
import yaml

from presenters.CameraFeedbackPresenter import CameraFeedbackPresenter

class CameraFeedbackScreen(Screen):
    
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
            
    fonts = paths['assets']['fonts']
    icons = paths['assets']['icons']
        
    Builder.load_file('views/screens/CameraFeedbackScreen.kv')

    def __init__(self, **kwargs):
        super(CameraFeedbackScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        
        CameraFeedbackPresenter(self)
        
        self.logs = []
        
        self.bind(size = self.resize)   
        
    def set_presenter(self, presenter):
        self.presenter = presenter     
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def switch_to_home_screen(self):
        self.presenter.switch_to_home_screen()
        
    def switch_to_settings_screen(self):
        self.presenter.switch_to_settings_screen()
        
    def on_stop(self):
        self.presenter.on_stop()