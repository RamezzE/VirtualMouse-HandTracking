from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
import cv2
import numpy as np
from components.Camera import Camera
from components.RotatingSpinner import RotatingSpinner

from gesturePredictor import GesturePredictor as GP
from mouseController import MouseController as MC
from KalmanFilter import KalmanFilter1D as KF
import pyautogui
import yaml

screenSize = pyautogui.size()
import threading 

def prepareLandmarks(landmarks):
    x_values = np.array([landmark.x for landmark in landmarks])
    y_values = np.array([landmark.y for landmark in landmarks])

    if x_values.size > 0 and y_values.size > 0:
        x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
        y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

    arr = np.concatenate((x_values, y_values))
    return arr.reshape(1, -1)

class GestureControlPanel(FloatLayout):
    def __init__(self, **kwargs):
        super(GestureControlPanel, self).__init__(**kwargs)
        
        self.updateLog, self.lastAction = None, None
        
        self.camera = Camera(captureIndex = 0, fps=30, size_hint = (1, 1), pos_hint={'top':1})
        self.add_widget(self.camera)  

        
        with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
            
        icons = paths['assets']['icons']
        
        self.videoIcon = Image(
            source = icons['video'], 
            size_hint = (0.2, 0.2), 
            pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.spinner = RotatingSpinner(
            size_hint = (0.5, 0.5),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            numLines = 3,
            lineThickness = 2,
            animationDuration = 3,
            gap = 50,
            color = [18/255, 18/255, 18/255, 0.87]
        )
        
        self.add_widget(self.videoIcon)
        self.add_widget(self.spinner)
        
        self.threadLoaded = False
        self.thread = threading.Thread(target=self.loadComponents)
        self.thread.daemon = True
        self.thread.start()   
           
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

        if not self.threadLoaded:
            return
        
        self.remove_widget(self.spinner)
        self.remove_widget(self.videoIcon)

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
        
    def loadComponents(self):
        
        from tensorflow.keras.models import load_model
        
        self.model = load_model('model/model_no_z2.keras')
        
        self.GP = GP(self.model)
        
        from handDetector import HandDetector as HD
        self.HD = HD()
        self.MC = MC(screenSize)
        
        self.KF_x = KF()
        self.KF_y = KF()
        
        self.threadLoaded = True
        
        self.camera.startCapture()

    def on_stop(self):
        self.camera.stopCapture()
        self.thread.join()
