from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ObjectProperty

from components.Camera import Camera

from presenters import GestureDetectionPresenter as Presenter 

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
        
        self.camera = Camera(
            captureIndex=0,
            size_hint=(1, 0.9),
            pos_hint={'top': 1}
        )
        
        self.add_widget(self.camera)
        
    def set_presenter(self, presenter):
        self.presenter = presenter

    def show_loading(self, message):
        self.show_loading_spinner = True
        self.status = message

    def hide_loading(self, message):
        self.show_loading_spinner = False
        self.status = message

    def show_frame(self, frame):
        self.camera.show_frame(frame)
        
    def update_fps(self, fps):
        self.current_fps = fps
        
    def on_stop(self):
        self.camera.stop_capture()
        
    def update_settings(self):
        self.presenter.update_settings()