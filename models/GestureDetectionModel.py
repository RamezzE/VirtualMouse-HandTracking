from kivy.app import App

from modules.GesturePredictor import GesturePredictor as GP
from modules.MouseController import MouseController as MC
from modules.KalmanFilter import KalmanFilter1D as KF

import pyautogui
import threading
import numpy as np
import cv2

class GestureDetetctionModel:
    
    def __init__(self, on_load):
        self.db = App.get_running_app().db

        self.actions = np.array(self.db.get('Actions', columns_to_select='name')).reshape(-1)
        self.mappings = np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)
        self.detection_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Confidence')[0])
        self.tracking_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Tracking Confidence')[0])
        self.buffer_size = int(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Responsiveness')[0])
        self.relative_mouse_sensitivity = float(self.db.get('MouseSettings', columns_to_select=['value'], name='Relative Mouse Sensitivity')[0])
        self.relative_mouse = self.db.get('MouseSettings', columns_to_select=['value'], name='Relative Mouse')[0]
        
        self.relative_mouse = True if self.relative_mouse == 1 else False
        
        self.last_action_index = None
        self.last_prediction = None
        
        self.on_load = on_load
        
        threading.Thread(target=self._load_components).start()
        
    @property
    def action_types(self):
        return {
            'IDLE': 0,
            'DRAG': 1,
            'MOVE_MOUSE': 2,
            'RIGHT_CLICK': 3,
            'LEFT_CLICK': 4,
            'DOUBLE_CLICK': 5,
            'ZOOM': 6,
            'SCROLL_UP': 7,
            'SCROLL_DOWN': 8,
            'TOGGLE_RELATIVE_MOUSE': 9
        }
        
    @property
    def gestures(self):
        return {
            'INDEX': 0,
            'INDEX_MIDDLE':1,
            'INDEX_THUMB': 2,
            'INDEX_MIDDLE_THUMB': 3,
            'PEACE': 4,
            'HAND_OPEN': 5,
            'FIST': 6,
            'PINCH': 7,
            'THUMBS_UP': 8,
            'THUMBS_DOWN': 9,
            'THUMBS_PINKY': 10
        }

    def _load_components(self):
        
        # from tensorflow.keras.models import load_model
        import pickle as pkl
        from modules.HandDetector import HandDetector as HD
        
        paths = App.get_running_app().paths
        
        self.model = pkl.load(open(paths['model'], "rb"))
        self.pca = pkl.load(open(paths['pca'], "rb"))
        self.HD = HD(detection_con=self.detection_confidence, track_con=self.tracking_confidence)
        self.GP = GP(self.model, self.buffer_size, is_tf = False, pca = self.pca)
        self.MC = MC(pyautogui.size(), self.relative_mouse_sensitivity, self.relative_mouse)
        self.KF_x = KF()
        self.KF_y = KF()
        
        self.on_load()

    def get_action(self, prediction):
        return (self.actions[self.mappings[prediction] - 1]), (self.mappings[prediction] - 1)

    def predict(self, landmarks, is_left_hand = False):
        return self.GP.predict(landmarks, is_left_hand)

    def process_frame(self, frame, draw_connections = False):
        frame = cv2.flip(frame, 1)
        frame = self.HD.find_hands(img=frame, draw_connections=draw_connections)
        landmarks = self.HD.get_landmarks()
        return frame, landmarks

    def get_hand_orientation(self):
        return self.HD.get_hand_orientation()
        
    def reset_kalman_filter(self):
        self.KF_x.reset()
        self.KF_y.reset()
        
    def highlight_gesture(self, frame, prediction):
        
        if prediction == self.gestures['INDEX']:
            fingers = [self.HD.INDEX]
        elif prediction == self.gestures['INDEX_MIDDLE']:
            fingers = [self.HD.INDEX, self.HD.MIDDLE]
        elif prediction == self.gestures['INDEX_THUMB']:
            fingers = [self.HD.INDEX, self.HD.THUMB]
        elif prediction == self.gestures['INDEX_MIDDLE_THUMB']:
            fingers = [self.HD.INDEX, self.HD.MIDDLE, self.HD.THUMB]
        elif prediction == self.gestures['PEACE']:
            fingers = [self.HD.INDEX, self.HD.MIDDLE]
        elif prediction == self.gestures['HAND_OPEN'] or prediction == self.gestures['FIST']:
            fingers = [self.HD.THUMB, self.HD.INDEX, self.HD.MIDDLE, self.HD.RING, self.HD.PINKY]
        elif prediction == self.gestures['PINCH']:
            fingers = [self.HD.THUMB, self.HD.INDEX]
        elif prediction == self.gestures['THUMBS_UP'] or prediction == self.gestures['THUMBS_DOWN']:
            fingers = [self.HD.THUMB]
        elif prediction == self.gestures['THUMBS_PINKY']:
            fingers = [self.HD.THUMB, self.HD.PINKY]
        else:
            fingers = []
            
        return self.HD.highlight_fingers(frame, fingers)
        
    def execute_action(self, action_index, frame):
        if action_index == self.action_types['IDLE'] or action_index is None:
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()
            self.MC.reset_mouse_pos()
            return
        
        if action_index == self.action_types['LEFT_CLICK']:
            self.MC.click_mouse(button='left')
            self.MC.reset_click(button='right')
            self.MC.reset_mouse_pos()
            return
        
        if action_index == self.action_types['RIGHT_CLICK']:
            self.MC.click_mouse(button='right')
            self.MC.reset_click(button='left')
            self.MC.reset_mouse_pos()
            return
        
        if action_index == self.action_types['DOUBLE_CLICK']:
            self.MC.double_click(button='left')
            self.MC.reset_click(button='right')
            self.MC.reset_mouse_pos()
            return
        
        if action_index in (self.action_types['SCROLL_UP'], self.action_types['SCROLL_DOWN']):
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()
            self.MC.reset_mouse_pos()
            return
        
        if action_index == self.action_types['ZOOM']:
            return
        
        if action_index == self.action_types['TOGGLE_RELATIVE_MOUSE']:
            self.MC.toggle_relative_mouse()
            return
        
        if action_index == self.action_types['MOVE_MOUSE']:
            self.MC.handle_mouse_press(False)
            self.MC.reset_click()

        elif action_index == self.action_types['DRAG']:
            self.MC.handle_mouse_press(True)
            self.MC.reset_click()

        index_pos = self.HD.get_finger_position(self.HD.INDEX)

        if index_pos is not None:
            x, y = index_pos
            x = self.KF_x.update(x)
            y = self.KF_y.update(y)
            self.MC.move_mouse((x, y), frame.shape)

        return
    
    def update_settings(self, detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse):

        self.mappings = mappings

        try:
            if self.buffer_size != detection_responsiveness:
                self.buffer_size = detection_responsiveness
                self.GP.set_buffer_size(self.buffer_size)
                
        except:
            print('Error updating detection responsiveness')
            
        try:
            if self.detection_confidence != detection_confidence or self.tracking_confidence != tracking_confidence:
                self.detection_confidence = detection_confidence
                self.tracking_confidence = tracking_confidence
                self.HD.set_confidence(detection_confidence, tracking_confidence)
        except:
            print('Error updating detection and/or tracking confidence')
            
        try:
            if self.relative_mouse_sensitivity != relative_mouse_sensitivity:
                self.relative_mouse_sensitivity = relative_mouse_sensitivity  
                self.MC.set_relative_mouse_sensitivity(relative_mouse_sensitivity)
        except:
            print('Error updating relative mouse sensitivity')
            
        try:
            if self.relative_mouse != relative_mouse:
                self.relative_mouse = relative_mouse
                self.MC.toggle_relative_mouse()
        except:
            print('Error toggle relative mouse')