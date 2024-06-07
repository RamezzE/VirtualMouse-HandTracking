from kivy.clock import Clock
import cv2
import threading
import numpy as np

class CameraPresenter:
    
    def __init__(self, view):
        self.view = view
        self.view.set_presenter(self)
        
        self.capture_index = 0
        self.running = False
        self.latest_frame = None
        
    def start_capture(self):
        if self.view.running:
            return
        
        self.capture = cv2.VideoCapture(self.capture_index)
        
        try:
            self.view.set_running(True)
            self.capture_thread = threading.Thread(target=self.capture_frames)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
        except Exception as e:
            print(f'Error starting the camera: {e}')
        
    def stop_capture(self):
        if not self.running:
            return
        try:
            self.view.set_running(False)
            self.capture_thread.join()
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
        
    staticmethod
    def get_available_cameras(n = 10):
        available_cameras = []
        for i in range(n):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        return available_cameras
    