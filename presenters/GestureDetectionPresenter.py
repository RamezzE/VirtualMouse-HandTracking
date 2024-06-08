from kivy.app import App
from kivy.clock import Clock
import cv2
from models.GestureDetectionModel import GestureDetetctionModel as Model

class GestureDetectionPresenter:
    def __init__(self, view):

        self.model = Model(self.on_dependencies_loaded, None)
        self.view = view
        
        self.dependencies_loaded = False
        self.saving_settings = False
        
        Clock.schedule_interval(self.update, 0)
        
    def on_dependencies_loaded(self):
        self.dependencies_loaded = True
        add_log_func = App.get_running_app().sm.get_screen('camera').add_log
        self.model.add_log = add_log_func
        Clock.schedule_once(self.update_status, 0)

    def update_status(self, dt = 0):
        if not self.dependencies_loaded:
            self.view.show_loading("Loading dependencies...")
        elif self.saving_settings:
            self.view.show_loading("Saving settings...")
        else:
            self.view.hide_loading("Press the toggle button\n to start/stop camera feed")

    def update(self, dt):
        self.update_status()
        self.view.update_fps(int(Clock.get_rfps()))

        if not self.view.ids.camera.running or not self.dependencies_loaded:
            return  

        frame = self.view.ids.camera.get_latest_frame()
        
        if frame is not None:
            frame = cv2.flip(frame, 1)
            frame = self.model.HD.find_hands(img=frame, draw_connections=True)
            landmarks = self.model.HD.get_landmarks()
            
            if landmarks:
                prediction = self.model.GP.predict(landmarks)
                frame = self.model.handle_input(prediction, frame)

            self.view.show_frame(frame)
            
    def update_settings(self, detection_confidence, tracking_confidence, detection_responsiveness):
        self.model.update_settings(detection_confidence, tracking_confidence, detection_responsiveness)
        