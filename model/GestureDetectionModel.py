from kivy.app import App
import numpy as np

from gesturePredictor import GesturePredictor as GP
from mouseController import MouseController as MC
from KalmanFilter import KalmanFilter1D as KF

import pyautogui
import threading 

class GestureDetetctionModel:
    log = ''
    
    def __init__(self, callback, paths = ''):
        self.db = App.get_running_app().db

        self.paths = paths

        self.actions = np.array(self.db.get('Actions', columns_to_select='name')).reshape(-1)
        self.mappings = np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)
        self.detection_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Confidence')[0])
        self.tracking_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Tracking Confidence')[0])

        self.lastAction = None
        
        self.callback = callback
        
        threading.Thread(target=self._load_components).start()

    def _load_components(self):
        
        from tensorflow.keras.models import load_model
        
        self.model = load_model("model/tfv3.keras")
        
        self.GP = GP(self.model)
        
        from handDetector import HandDetector as HD
        self.HD = HD(detectionCon=self.detection_confidence, trackCon=self.tracking_confidence)
        self.MC = MC(pyautogui.size())
        
        self.KF_x = KF()
        self.KF_y = KF()
        
        self.callback()

    def get_action(self, prediction):
        return self.actions[self.mappings[prediction] - 1], self.mappings[prediction] - 1

    def handle_input(self, prediction, frame):
        if prediction is None:
            return frame

        frame = self.HD.highlightGesture(frame, prediction)
        actionName, actionIndex = self.get_action(prediction)

        if self.lastAction is None:
            self.lastAction = actionIndex
            self.log = actionName

        if actionIndex != self.lastAction:
            self.lastAction = actionIndex
            self.KF_x.reset()
            self.KF_y.reset()
            self.log = actionName

        else:
            if actionIndex == GP.TOGGLE_RELATIVE_MOUSE:
                return frame

        if actionIndex == GP.IDLE:
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            self.MC.resetMousePos()
            return frame

        if actionIndex == GP.LEFT_CLICK:
            self.MC.clickMouse(button='left')
            self.MC.resetClick(button='right')
            self.MC.resetMousePos()
            return frame

        if actionIndex == GP.RIGHT_CLICK:
            self.MC.clickMouse(button='right')
            self.MC.resetClick(button='left')
            self.MC.resetMousePos()
            return frame

        if actionIndex == GP.DOUBLE_CLICK:
            self.MC.doubleClick(button='left')
            self.MC.resetClick(button='right')
            self.MC.resetMousePos()
            return frame

        if actionIndex in (GP.SCROLL_UP, GP.SCROLL_DOWN):
            frame = self.HD.highlightFingers(img=frame, fingers=[self.HD.THUMB])
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            self.MC.resetMousePos()
            return frame

        if actionIndex == GP.ZOOM:
            return frame

        if actionIndex == GP.TOGGLE_RELATIVE_MOUSE:
            self.MC.toggleRelativeMouse()
            return frame

        if actionIndex == GP.MOVE_MOUSE:
            self.MC.handleMousePress(False)
            self.MC.resetClick()

        elif actionIndex == GP.DRAG:
            self.MC.handleMousePress(True)
            self.MC.resetClick()

        IndexPos = self.HD.getFingerPosition(self.HD.INDEX)

        if IndexPos is not None:
            x, y = IndexPos
            x = self.KF_x.update(x)
            y = self.KF_y.update(y)
            self.MC.moveMouse((x, y), frame.shape)

        return frame
    
    def update_settings(self, detection_confidence, tracking_confidence):
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.HD.setCon(detection_confidence, tracking_confidence)
        
        # self.db.update('DetectionSettings', 'value', detection_confidence, name='Detection Confidence')
        # self.db.update('DetectionSettings', 'value', tracking_confidence, name='Tracking Confidence')