import cv2
from handDetector import HandDetector
from mouseController import MouseController
from gesturePredictor import GesturePredictor
from KalmanFilter import KalmanFilter1D

from tensorflow.keras.models import load_model

import pyautogui
import numpy as np
import time
import pickle
import pandas as pd

model = load_model('model/model_no_z.keras')

# model = pickle.load(open('model/decision_tree.pkl', 'rb'))

import warnings
# Suppress warnings
# warnings.filterwarnings('ignore')

screenSize = pyautogui.size()

HD = HandDetector()
MC = MouseController(screenSize)
GP = GesturePredictor(model)
KF_x = KalmanFilter1D()
KF_y = KalmanFilter1D()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

arr = ['idle', 'left_click', 'right_click', 'move_mouse', 'press_and_hold_left_click', 'pinch', 'scroll', 'double_click']

IDLE = 0
LEFT_CLICK = 1
RIGHT_CLICK = 2
MOVE_MOUSE = 3
PRESS_AND_HOLD_LEFT_CLICK = 4
PINCH = 5
SCROLL = 6
DOUBLE_LEFT_CLICK = 7


def preprocess(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    return [(val - min_val) / (max_val - min_val) for val in arr]

def prepareLandmarks(landmarks):
    x_values = []
    y_values = []
    
    arr = []
    
    for landmark in landmarks:
        x_values.append(landmark.x)
        y_values.append(landmark.y)
        
    if x_values != [] and y_values != []:
        x_values_normalized = preprocess(x_values)
        y_values_normalized = preprocess(y_values)
    
    arr = np.concatenate((x_values_normalized, y_values_normalized))
    
    arr = np.array(arr)
    arr = arr.reshape(1, -1)
    
    return arr

last_prediction = None

def handleInput(prediction, frame):
    global last_prediction
    
    if last_prediction is None:
        last_prediction = prediction
        print(arr[prediction])
    
    if prediction != last_prediction:
        last_prediction = prediction
        
        print(arr[prediction])
    
    if prediction == IDLE:
        MC.handleMousePress(False)
        MC.resetClick()
        return frame
    
    if prediction == LEFT_CLICK:
        MC.clickMouse(button = 'left')
        MC.resetClick(button = 'right')
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE, HD.THUMB])
    
    if prediction == RIGHT_CLICK:
        MC.clickMouse(button = 'right') 
        MC.resetClick(button = 'left')
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.THUMB])
    
    if prediction == DOUBLE_LEFT_CLICK:
        MC.doubleClick(button = 'left')
        
        MC.resetClick(button = 'right')
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE])
            
    if prediction == SCROLL:
        frame = HD.highlightFingers(img = frame, fingers = [HD.THUMB])
        MC.handleMousePress(False)
        MC.resetClick()
        # MC.handleScroll()
        return frame
    
    if prediction == PINCH:
        pass
        
    if prediction == MOVE_MOUSE:
        # if (HD.isDistanceWithin(HD.INDEX, HD.MIDDLE)):
        MC.handleMousePress(False)
        MC.resetClick()
        frame = HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE])
    
    elif prediction == PRESS_AND_HOLD_LEFT_CLICK:
        MC.handleMousePress(True)
        MC.resetClick()
        frame = HD.highlightFingers(img = frame, fingers = [HD.INDEX])
        
    IndexPos = HD.getFingerPosition(HD.INDEX)
    
    if IndexPos is not None:
        x, y = IndexPos
        x = KF_x.update(x)
        y = KF_y.update(y)
        MC.moveMouse((x, y), frame.shape)
    
    # MC.moveMouse(HD.getFingerPosition(HD.INDEX), frame.shape)
    return frame

while True:
    start_time = time.time()
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
    
    landmarks = HD.getLandmarks()
    
    if landmarks:
        landmarks = prepareLandmarks(landmarks)
        y_pred = GP.predict(landmarks)
        frame = handleInput(y_pred, frame)
    
    cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)
    
    # Show fps on screen
    fps = 1.0 / (time.time() - start_time)
    
    frame = cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
        
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()