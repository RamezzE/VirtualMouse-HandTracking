from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.properties import BooleanProperty
import cv2

from presenters import CameraPresenter

class CameraView(Image):
    
    running = BooleanProperty(False)
    capture = None
    
    def __init__(self, **kwargs):
        super(CameraView, self).__init__(**kwargs)
        
        CameraPresenter(self)
    
    def show_frame(self, frame):
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
        
    def set_presenter(self, presenter):
        self.presenter = presenter
        
    def set_running(self, running):
        self.running = running
        
    def toggle_capture(self):
        self.presenter.toggle_capture()
        
    def get_latest_frame(self):
        return self.presenter.latest_frame
        
    def on_stop(self):
        self.presenter.stop_capture()
        