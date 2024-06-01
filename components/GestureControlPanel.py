from kivy.uix.accordion import ObjectProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import cv2
import numpy as np
from components.Camera import Camera

from handDetector import HandDetector
from gesturePredictor import GesturePredictor as GP
from mouseController import MouseController as MC
from KalmanFilter import KalmanFilter1D as KF
import pyautogui

screenSize = pyautogui.size()

from tensorflow.keras.models import load_model

model = load_model('model/model_no_z2.keras')

def prepareLandmarks(landmarks):
    x_values = np.array([landmark.x for landmark in landmarks])
    y_values = np.array([landmark.y for landmark in landmarks])

    if x_values.size > 0 and y_values.size > 0:
        x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
        y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

    arr = np.concatenate((x_values, y_values))
    return arr.reshape(1, -1)

class GestureControlPanel(FloatLayout):
    callback = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(GestureControlPanel, self).__init__(**kwargs)
        
        self.camera = Camera(captureIndex = 0, fps=30, size_hint = (1, 1), pos_hint={'top':1})
        self.HD = HandDetector()
        self.MC = MC(screenSize)
        self.GP = GP(model)
        
        self.KF_x = KF()
        self.KF_y = KF()
        
        self.updateLog = None
                
        self.add_widget(self.camera)   
        
        self.lastAction = None
                
        Clock.schedule_interval(self.update, 1.0 / 30)
    
    def handleInput(self, prediction, frame):
        if prediction is None:
            return frame
        
        frame = self.HD.highlightGesture(frame, prediction)
        
        actionName, actionIndex = self.GP.getAction(prediction)
        
        if self.lastAction is None:
            self.lastAction = actionIndex
            if self.updateLog is not None: self.updateLog(actionName)
            # print(actionName)
                
        if actionIndex != self.lastAction:
            self.lastAction = actionIndex
            self.KF_x.reset()
            self.KF_y.reset()
            if self.updateLog is not None: self.updateLog(actionName)
            # print(actionName)                
        
        if actionIndex == GP.IDLE:
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            self.MC.resetMousePos()
            return frame
        
        if actionIndex == GP.LEFT_CLICK:
            self.MC.clickMouse(button = 'left')
            self.MC.resetClick(button = 'right')
            self.MC.resetMousePos()
            return frame
            # return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE, self.HD.THUMB])
        
        if actionIndex == GP.RIGHT_CLICK:
            self.MC.clickMouse(button = 'right') 
            self.MC.resetClick(button = 'left')
            self.MC.resetMousePos()
            return frame 
            # return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.THUMB])
        
        if actionIndex == GP.DOUBLE_LEFT_CLICK:
            self.MC.doubleClick(button = 'left')
            
            self.MC.resetClick(button = 'right')
            self.MC.resetMousePos()
            return frame
            # return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE])
                
        if actionIndex == GP.SCROLL:
            frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.THUMB])
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            # MC.handleScroll()
            self.MC.resetMousePos()
            return frame
        
        if actionIndex == GP.PINCH:
            return frame
            
        if actionIndex == GP.MOVE_MOUSE:
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            # frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE])
        
        elif actionIndex == GP.DRAG:
            self.MC.handleMousePress(True)
            self.MC.resetClick()
            # frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX])
            
        IndexPos = self.HD.getFingerPosition(self.HD.INDEX)
        
        if IndexPos is not None:
            x, y = IndexPos
            x = self.KF_x.update(x)
            y = self.KF_y.update(y)
            self.MC.moveMouse((x, y), frame.shape)
        
        return frame
        
    def update(self, dt):
        frame = self.camera.getLatestFrame()
        
        if frame is not None:
            frame = cv2.flip(frame, 1)
            frame = self.HD.findHands(img=frame, drawConnections=True)
            landmarks = self.HD.getLandmarks()
            
            if landmarks:
                landmarks = prepareLandmarks(landmarks)
                prediction = self.GP.predict(landmarks)
                frame = self.handleInput(prediction, frame)

            self.camera.showFrame(frame)
        
    def on_stop(self):
        self.camera.releaseCamera()