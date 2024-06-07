from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty

from presenters import GestureDetectionPresenter as Presenter
from views.components import CameraView, RotatingSpinner

import yaml

from kivy.lang import Builder

class GestureDetectionView(FloatLayout):
    show_loading_spinner = BooleanProperty(False)
    current_fps = NumericProperty()
    status = StringProperty()
        
    with open('paths.yaml', 'r') as f:
        paths = yaml.safe_load(f)
        
    icons = paths['assets']['icons']
    fonts = paths['assets']['fonts']
    
    Builder.load_file('views/components/GestureDetectionView.kv')
    
    def __init__(self, **kwargs):
        super(GestureDetectionView, self).__init__(**kwargs)
                
        self.presenter = Presenter(self)
        
    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_loading(self, message):
        self.show_loading_spinner = True
        self.status = message

    def hide_loading(self, message):
        self.show_loading_spinner = False
        self.status = message

    def show_frame(self, frame):
        self.ids.camera.show_frame(frame)
        
    def update_fps(self, fps):
        self.current_fps = fps
        
    def on_stop(self):
        self.ids.camera.on_stop()
        
    def update_settings(self):
        self.presenter.update_settings()