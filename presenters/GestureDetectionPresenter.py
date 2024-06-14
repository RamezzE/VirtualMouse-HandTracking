from kivy.clock import Clock
from models.GestureDetectionModel import GestureDetetctionModel

class GestureDetectionPresenter:
    def __init__(self, view):

        self.model = GestureDetetctionModel(self.on_dependencies_loaded)
        self.view = view
        
        self.action_types = self.model.action_types
        
        self.dependencies_loaded = False
        self.saving_settings = False
        
        self.last_prediction = None
        self.last_action_index = None
        self.add_log = None
        
        Clock.schedule_interval(self.update, 0)
        
    def set_log_callback(self, callback):
        self.add_log = callback
        
    def set_saving_settings(self, value):
        self.saving_settings = value
        
    def on_dependencies_loaded(self):
        self.dependencies_loaded = True
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

        if not self.view.is_camera_running() or not self.dependencies_loaded:
            return  

        frame = self.view.get_latest_frame()
        
        if frame is None:
            return
        
        frame, landmarks = self.model.process_frame(frame, draw_connections=True)
        if landmarks:
            is_left_hand = self.model.get_hand_orientation() == "Left"
            prediction = self.model.predict(landmarks, is_left_hand = is_left_hand)   
            frame = self.handle_input(prediction, frame)

        self.view.show_frame(frame)
            
    def handle_input(self, prediction, frame):
        if prediction is None:
            return frame
        
        frame = self.model.highlight_gesture(frame, prediction)
        action_name, action_index = self.model.get_action(prediction)

        if self.last_action_index is None:
            self.last_action_index = action_index
                
        elif prediction != self.last_prediction:
            self.last_prediction = prediction
            
            if self.add_log is not None:
                self.add_log(int(prediction), action_name)

        if action_index != self.last_action_index:
            self.last_action_index = action_index
            self.model.reset_kalman_filter()

        elif action_index == self.action_types['TOGGLE_RELATIVE_MOUSE']:
            return frame
        
        if action_index == self.action_types['TOGGLE_RELATIVE_MOUSE']:
            self.view.toggle_relative_mouse()
        
        self.model.execute_action(action_index, frame)
            
        return frame
            
    def update_settings(self, detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse):
        self.model.update_settings(detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse)