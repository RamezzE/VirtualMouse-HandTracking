from kivy.uix.accordion import BooleanProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.lang import Builder

import threading 
import cv2
import numpy as np
import pyautogui
import yaml

from components.CustomButton import CustomButton
from components.Camera import Camera
from components.RotatingSpinner import RotatingSpinner
from gesturePredictor import GesturePredictor as GP
from mouseController import MouseController as MC
from KalmanFilter import KalmanFilter1D as KF

class GestureControlPanel(FloatLayout):
    
    threadLoaded = BooleanProperty(False)
    
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
        
    icons = paths['assets']['icons']
    fonts = paths['assets']['fonts']

    Builder.load_file('kv/components/GestureControlPanel.kv')
    
    def __init__(self, **kwargs):
        super(GestureControlPanel, self).__init__(**kwargs)

        self.updateLog, self.lastAction = None, None
        
        self.threadLoaded = False
        
        self.camera = Camera(
            captureIndex = 0,
            fps= 30 ,
            size_hint= (1, 0.9),
            pos_hint= {'top':1}
        )
        
        self.add_widget(self.camera)

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
        else:
            if actionIndex == GP.TOGGLE_RELATIVE_MOUSE:
                return frame
        
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
        
        if actionIndex == GP.RIGHT_CLICK:
            self.MC.clickMouse(button = 'right') 
            self.MC.resetClick(button = 'left')
            self.MC.resetMousePos()
            return frame 
        
        if actionIndex == GP.DOUBLE_CLICK:
            self.MC.doubleClick(button = 'left')
            
            self.MC.resetClick(button = 'right')
            self.MC.resetMousePos()
            return frame
                
        if actionIndex == GP.SCROLL_UP or actionIndex == GP.SCROLL_DOWN:
            frame = self.HD.highlightFingers(img = frame, fingers = [self.HD.THUMB])
            self.MC.handleMousePress(False)
            self.MC.resetClick()
            # MC.handleScroll()
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
        
    def update(self, dt):

        if not self.threadLoaded:
            return

        frame = self.camera.getLatestFrame()
        
        if frame is not None:
            frame = cv2.flip(frame, 1)
            frame = self.HD.findHands(img=frame, drawConnections=True)
            landmarks = self.HD.getLandmarks()
            
            if landmarks:
                prediction = self.GP.predict(landmarks)
                frame = self.handleInput(prediction, frame)

            self.camera.showFrame(frame)        
        
    def loadComponents(self):
        
        from tensorflow.keras.models import load_model
        
        self.model = load_model(self.paths['model'])
        
        self.GP = GP(self.model)
        
        from handDetector import HandDetector as HD
        self.HD = HD()
        self.MC = MC(pyautogui.size())
        
        self.KF_x = KF()
        self.KF_y = KF()
        
        Clock.schedule_once(self.set_threadLoaded)

    def set_threadLoaded(self, dt):
        self.threadLoaded = True      
        
    def on_stop(self):
        self.camera.stopCapture()
        
    def startCamera(self):
        self.camera.startCapture()
    
