from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

import queue
import cv2
import threading

class Camera(Image):
    def __init__(self, captureIndex, fps, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(captureIndex)
        self.fps = fps
        
        self.frame_queue = queue.Queue(maxsize = 3)
                
        self.capture_thread = threading.Thread(target = self.capture_frames)
        self.capture_thread.start()
        
    def capture_frames(self):
        try:
            while self.capture.isOpened():
                ret, frame = self.capture.read()
                if not ret:
                    break
                
                if self.frame_queue.full():
                    self.frame_queue.get_nowait()
                    
                self.frame_queue.put(frame)
                
        except Exception as e:
            print(f'Capture thread error: {e}')
            
        finally:
            self.capture.release()
            cv2.destroyAllWindows()
            print('Capture thread released the camera')
            
    def getLatestFrame(self):
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        
        return None
    
    def showFrame(self, frame):
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = texture
        
    def releaseCamera(self):
        self.frame_queue.queue.clear()
        self.capture.release()