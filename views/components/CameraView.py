from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2

from presenters import CameraPresenter

class CameraView(Image):
    running = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(CameraView, self).__init__(**kwargs)
        self.presenter = CameraPresenter(self)
    
    def show_frame(self, frame):
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
        
    def toggle_capture(self):
        self.presenter.toggle_capture()
        
    def get_latest_frame(self):
        return self.presenter.get_latest_frame()
    
    def set_running(self, value):
        self.running = value
    
    def is_running(self):
        return self.presenter.is_running()
    
    def start(self):
        self.presenter.start_capture()
        
    def stop(self):
        self.presenter.stop_capture()