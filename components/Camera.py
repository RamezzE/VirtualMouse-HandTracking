from kivy.uix.accordion import BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import cv2
import threading
import numpy as np

class Camera(Image):
    
    captureIndex = NumericProperty(0)
    running = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        
        self.running = False
        self.latest_frame = None
        
    def start_capture(self):
        if self.running:
            return
        self.capture = cv2.VideoCapture(self.captureIndex)
        
        try:
            self.running = True
            self.captureThread = threading.Thread(target=self.capture_frames)
            self.captureThread.daemon = True
            self.captureThread.start()
        except Exception as e:
            print(f'Error starting the camera: {e}')
        
    def stop_capture(self):
        if not self.running:
            return
        try:
            self.running = False
            self.captureThread.join()
            white_frame = 255 * np.ones((480, 640, 3), np.uint8)
            Clock.schedule_once(lambda dt: self.show_frame(white_frame), 0) 
            
        except Exception as e:
            print(f'Error stopping the camera: {e}')
        
    def toggle_capture(self):
        if self.running:
            self.stop_capture()
        else:
            self.start_capture()
        
    def capture_frames(self):
        try:
            while self.capture.isOpened() and self.running:
                
                ret, self.latest_frame = self.capture.read()
                if not ret:
                    break            
    
                
        except Exception as e:
            print(f'Capture thread error: {e}')
        
        finally:
            self.stop_capture()
            print('Capture thread released the camera')
            
    def get_latest_frame(self):
        frame = self.latest_frame
        self.latest_frame = None
        return frame
    
    def show_frame(self, frame):
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
        
    staticmethod
    def get_available_cameras(n = 10):
        available_cameras = []
        for i in range(n):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
    