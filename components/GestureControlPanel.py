from kivy.uix.accordion import ObjectProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import cv2
import numpy as np
from components.Camera import Camera

from handDetector import HandDetector
from gesturePredictor import GesturePredictor
from mouseController import MouseController
from KalmanFilter import KalmanFilter1D
import pyautogui

arr = ['idle', 'left_click', 'right_click', 'move_mouse', 'press_and_hold_left_click', 'pinch', 'scroll', 'double_click']

IDLE = 0
LEFT_CLICK = 1
RIGHT_CLICK = 2
MOVE_MOUSE = 3
PRESS_AND_HOLD_LEFT_CLICK = 4
PINCH = 5
SCROLL = 6
DOUBLE_LEFT_CLICK = 7
screenSize = pyautogui.size()

from tensorflow.keras.models import load_model


model = load_model('model/model_no_z.keras')

def preprocess(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    return [(val - min_val) / (max_val - min_val) for val in arr]

def prepareLandmarks(landmarks):
    x_values = np.array([landmark.x for landmark in landmarks])
    y_values = np.array([landmark.y for landmark in landmarks])

    if x_values.size > 0 and y_values.size > 0:
        x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
        y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

    arr = np.concatenate((x_values, y_values))
    return arr.reshape(1, -1)

class GestureControlPanel(FloatLayout):
    camera = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(GestureControlPanel, self).__init__(**kwargs)
        
        self.camera = Camera(captureIndex = 0, fps=30, size_hint = (1, 1), pos_hint={'top':1})
        self.HD = HandDetector()
        self.MC = MouseController(screenSize)
        self.GP = GesturePredictor(model)
        
        self.KF_x = KalmanFilter1D()
        self.KF_y = KalmanFilter1D()
                
        self.add_widget(self.camera)   
        
        self.last_prediction = None
                
        Clock.schedule_interval(self.update, 1.0 / 30)
        
    def handleInput(self, prediction, frame):
        
        if self.last_prediction is None:
            self.last_prediction = prediction
            print(arr[prediction])
        
        if prediction != self.last_prediction:
            self.last_prediction = prediction
            self.KF_x.reset()
            self.KF_y.reset()
            
            print(arr[prediction])
        
        if prediction == IDLE:
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            self.MC.resetMousePos()
            return frame
        
        if prediction == LEFT_CLICK:
            self.MC.clickMouse(button = 'left')
            self.MC.resetClick(button = 'right')
            self.MC.resetMousePos()
            return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE, self.HD.THUMB])
        
        if prediction == RIGHT_CLICK:
            self.MC.clickMouse(button = 'right') 
            self.MC.resetClick(button = 'left')
            self.MC.resetMousePos()
            return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.THUMB])
        
        if prediction == DOUBLE_LEFT_CLICK:
            self.MC.doubleClick(button = 'left')
            
            self.MC.resetClick(button = 'right')
            self.MC.resetMousePos()
            return self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE])
                
        if prediction == SCROLL:
            frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.THUMB])
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            # MC.handleScroll()
            self.MC.resetMousePos()
            return frame
        
        if prediction == PINCH:
            return frame
            
        if prediction == MOVE_MOUSE:
            # if (HD.isDistanceWithin(HD.INDEX, HD.MIDDLE)):
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX, self.HD.MIDDLE])
        
        elif prediction == PRESS_AND_HOLD_LEFT_CLICK:
            self.MC.handleMousePress(True)
            self.MC.resetClick()
            frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.INDEX])
            
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