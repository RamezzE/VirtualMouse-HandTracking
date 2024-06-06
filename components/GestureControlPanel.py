from kivy.uix.accordion import NumericProperty
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.app import App

import threading
import cv2
import numpy as np
import pyautogui
import yaml
import time

from components.CustomButton import CustomButton
from components.Camera import Camera
from components.RotatingSpinner import RotatingSpinner
from gesturePredictor import GesturePredictor as GP
from mouseController import MouseController as MC
from KalmanFilter import KalmanFilter1D as KF

class GestureControlPanel(FloatLayout):
    
    thread_loaded, saving_settings, show_loading = BooleanProperty(False), BooleanProperty(False), BooleanProperty(True) 
    
    status, current_fps = StringProperty(), StringProperty()
        
    with open('paths.yaml', 'r') as f:
            paths = yaml.safe_load(f)
        
    icons = paths['assets']['icons']
    fonts = paths['assets']['fonts']

    Builder.load_file('kv/components/GestureControlPanel.kv')
    
    def __init__(self, **kwargs):
        super(GestureControlPanel, self).__init__(**kwargs)
        
        self.db = App.get_running_app().db

        self.actions = (np.array(self.db.get('Actions', columns_to_select='name'))).reshape(-1)
        self.mappings = np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)
        self.detection_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name = 'Detection Confidence')[0])
        self.tracking_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name = 'Tracking Confidence')[0])
                
        self.updateLog, self.lastAction = None, None
        
        self.thread_loaded = False
        
        self.camera = Camera(
            captureIndex = 0,
            size_hint= (1, 0.9),
            pos_hint= {'top':1}
        )
        
        self.add_widget(self.camera)

        self.thread = threading.Thread(target=self.loadComponents)
        self.thread.daemon = True
        self.thread.start()
        
        Clock.schedule_interval(self.update, 0)
        
    def update_status(self, dt = 0):
        if not self.thread_loaded:
            self.show_loading = True
            self.status = "Loading dependencies..."
        elif self.saving_settings:
            self.show_loading = True
            self.status = "Saving settings..."
        else:
            self.show_loading = False
            self.status = "Press the toggle button\n to start/stop camera feed"
        
        
    def getAction(self, prediction):
        return self.actions[self.mappings[prediction]-1], self.mappings[prediction]-1
    
    def handleInput(self, prediction, frame):
        if prediction is None:
            return frame
        
        frame = self.HD.highlightGesture(frame, prediction)
                
        actionName, actionIndex = self.getAction(prediction)
        
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
        self.update_status()
        self.current_fps = str(int(Clock.get_rfps()))


        if not self.camera.running or not self.thread_loaded:
            return  

        frame = self.camera.get_latest_frame()
        
        if frame is not None:
            frame = cv2.flip(frame, 1)
            frame = self.HD.findHands(img=frame, drawConnections=True)
            landmarks = self.HD.getLandmarks()
            
            if landmarks:
                prediction = self.GP.predict(landmarks)
                frame = self.handleInput(prediction, frame)

            self.camera.show_frame(frame)
            
        
    def loadComponents(self):
        
        from tensorflow.keras.models import load_model
        
        self.model = load_model(self.paths['model'])
        
        self.GP = GP(self.model)
        
        from handDetector import HandDetector as HD
        self.HD = HD(detectionCon=self.detection_confidence, trackCon=self.tracking_confidence)
        self.MC = MC(pyautogui.size())
        
        self.KF_x = KF()
        self.KF_y = KF()
        
        Clock.schedule_once(self.set_thread_loaded)

    def set_thread_loaded(self, dt):
        self.thread_loaded = True      
    
    def on_stop(self):
        self.camera.stop_capture()
        
    def start_camera(self):
        self.camera.start_capture()
        
    def update_settings(self):
        try:
            self.HD.setCon(self.detection_confidence, self.tracking_confidence)
        except:
            pass