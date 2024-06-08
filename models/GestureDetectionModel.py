from kivy.app import App
import numpy as np

from modules.GesturePredictor import GesturePredictor as GP
from modules.MouseController import MouseController as MC
from modules.KalmanFilter import KalmanFilter1D as KF


import pyautogui
import threading 

class GestureDetetctionModel:
    
    def __init__(self, callback, add_log):
        self.db = App.get_running_app().db

        self.actions = np.array(self.db.get('Actions', columns_to_select='name')).reshape(-1)
        self.mappings = np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)
        self.detection_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Confidence')[0])
        self.tracking_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Tracking Confidence')[0])
        self.buffer_size = int(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Responsiveness')[0])
        self.last_action_index = None
        self.last_prediction = None
        
        self.callback = callback
        self.add_log = add_log
        
        threading.Thread(target=self._load_components).start()

    def _load_components(self):
        
        from tensorflow.keras.models import load_model
        from modules.HandDetector import HandDetector as HD

        self.model = load_model("models/tfv3.keras")
        
        self.HD = HD(detection_con=self.detection_confidence, track_con=self.tracking_confidence)
        self.GP = GP(self.model, self.buffer_size)
        self.MC = MC(pyautogui.size())
        self.KF_x = KF()
        self.KF_y = KF()
        
        self.callback()

    def get_action(self, prediction):
        return self.actions[self.mappings[prediction] - 1], self.mappings[prediction] - 1

    def handle_input(self, prediction, frame):
        if prediction is None:
            return frame

        frame = self.HD.highlight_gesture(frame, prediction)
        actionName, action_index = self.get_action(prediction)

        if self.last_action_index is None:
            self.last_action_index = action_index
                
        elif prediction != self.last_prediction:
            self.last_prediction = prediction
            
            if self.add_log is not None:
                self.add_log(int(prediction), actionName)

        if action_index != self.last_action_index:
            self.last_action_index = action_index
            self.KF_x.reset()
            self.KF_y.reset()

        elif action_index == GP.TOGGLE_RELATIVE_MOUSE:
            return frame

        if action_index == GP.IDLE:
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()
            self.MC.reset_mouse_pos()
            return frame

        if action_index == GP.LEFT_CLICK:
            self.MC.click_mouse(button='left')
            self.MC.reset_click(button='right')
            self.MC.reset_mouse_pos()
            return frame

        if action_index == GP.RIGHT_CLICK:
            self.MC.click_mouse(button='right')
            self.MC.reset_click(button='left')
            self.MC.reset_mouse_pos()
            return frame

        if action_index == GP.DOUBLE_CLICK:
            self.MC.double_click(button='left')
            self.MC.reset_click(button='right')
            self.MC.reset_mouse_pos()
            return frame

        if action_index in (GP.SCROLL_UP, GP.SCROLL_DOWN):
            frame = self.HD.highlight_fingers(img=frame, fingers=[self.HD.THUMB])
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()
            self.MC.reset_mouse_pos()
            return frame

        if action_index == GP.ZOOM:
            return frame

        if action_index == GP.TOGGLE_RELATIVE_MOUSE:
            self.MC.toggle_relative_mouse()
            return frame

        if action_index == GP.MOVE_MOUSE:
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()

        elif action_index == GP.DRAG:
            self.MC.handle_mouse_press(True)
            self.MC.reset_click()

        IndexPos = self.HD.get_finger_position(self.HD.INDEX)

        if IndexPos is not None:
            x, y = IndexPos
            x = self.KF_x.update(x)
            y = self.KF_y.update(y)
            self.MC.move_mouse((x, y), frame.shape)

        return frame
    
    def update_settings(self, detection_confidence, tracking_confidence, detection_responsiveness):
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.buffer_size = detection_responsiveness
                
        try:
            self.HD.set_confidence(detection_confidence, tracking_confidence)
            self.GP.set_buffer_size(detection_responsiveness)
        except:
            pass