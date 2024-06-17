from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty

from presenters import GestureDetectionPresenter
from views.components import CameraView, RotatingSpinner

from kivy.lang import Builder

class GestureDetectionView(FloatLayout):
    show_loading_spinner = BooleanProperty(False)
    current_fps = NumericProperty()
    status = StringProperty()
    
    Builder.load_file('views/components/GestureDetectionView.kv')
    
    def __init__(self, **kwargs):
        super(GestureDetectionView, self).__init__(**kwargs)
                
        self.presenter = GestureDetectionPresenter(self)
        
    def set_log_callback(self, callback):
        self.presenter.set_log_callback(callback)
        
    def set_saving_settings(self, value):
        self.presenter.set_saving_settings(value)

    def show_loading(self, message):
        self.show_loading_spinner = True
        self.status = message

    def hide_loading(self, message):
        self.show_loading_spinner = False
        self.status = message

    def show_frame(self, frame):
        self.ids['camera'].show_frame(frame)
        
    def update_fps(self, fps):
        self.current_fps = fps
        
    def update_settings(self, detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse, scroll_sensitivity):
        self.presenter.update_settings(detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse, scroll_sensitivity)    
        
    def start_camera(self):
        self.ids['camera'].start()
        
    def stop_camera(self):
        self.ids['camera'].stop()
        
    def is_camera_running(self):
        return self.ids['camera'].is_running()
    
    def get_latest_frame(self):
        return self.ids['camera'].get_latest_frame()
    
    def toggle_relative_mouse(self):
        self.parent.parent.manager.get_screen('settings').toggle_relative_mouse()
