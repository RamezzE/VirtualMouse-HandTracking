import cv2
from handDetector import HandDetector
from mouseController import MouseController
from gesturePredictor import GesturePredictor
from KalmanFilter import KalmanFilter1D

from tensorflow.keras.models import load_model

import pyautogui
import numpy as np
import time

import queue
import threading

model = load_model('model/model_no_z.keras')

screenSize = pyautogui.size()

HD = HandDetector()
MC = MouseController(screenSize)
GP = GesturePredictor(model)


MC.toggleRelativeMouse(True)

KF_x = KalmanFilter1D()
KF_y = KalmanFilter1D()

cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

frame_queue = queue.Queue(maxsize = 3)

def capture_frames(cap):
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_queue.full():
                # Discard the oldest frame (the one at the front of the queue)
                frame_queue.get_nowait()
            frame_queue.put(frame)
            
    except Exception as e:
        print(f'Capture thread error: {e}')
        
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print('Capture thread released the camera')

capture_thread = threading.Thread(target=capture_frames, args=(cap,))
capture_thread.start()

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
    x_values = np.array([landmark.x for landmark in landmarks])
    y_values = np.array([landmark.y for landmark in landmarks])

    if x_values.size > 0 and y_values.size > 0:
        x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
        y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

    arr = np.concatenate((x_values, y_values))
    return arr.reshape(1, -1)


last_prediction = None

def handleInput(prediction, frame):
    global last_prediction
    
    if last_prediction is None:
        last_prediction = prediction
        print(arr[prediction])
    
    if prediction != last_prediction:
        last_prediction = prediction
        KF_x.reset()
        KF_y.reset()
        
        print(arr[prediction])
    
    if prediction == IDLE:
        MC.handleMousePress(False)
        MC.resetClick()
        MC.resetMousePos()
        return frame
    
    if prediction == LEFT_CLICK:
        MC.clickMouse(button = 'left')
        MC.resetClick(button = 'right')
        MC.resetMousePos()
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE, HD.THUMB])
    
    if prediction == RIGHT_CLICK:
        MC.clickMouse(button = 'right') 
        MC.resetClick(button = 'left')
        MC.resetMousePos()
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.THUMB])
    
    if prediction == DOUBLE_LEFT_CLICK:
        MC.doubleClick(button = 'left')
        
        MC.resetClick(button = 'right')
        MC.resetMousePos()
        return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE])
            
    if prediction == SCROLL:
        frame = HD.highlightFingers(img = frame, fingers = [HD.THUMB])
        MC.handleMousePress(False)
        MC.resetClick()
        # MC.handleScroll()
        MC.resetMousePos()
        return frame
    
    if prediction == PINCH:
        return frame
        
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
    
    return frame

try:
    while True:
        start_time = time.time()
        
        frame = frame_queue.get()
        # _, frame = cap.read()
        
        frame = cv2.flip(frame, 1)
            
        frame = HD.findHands(img = frame, drawConnections = True)
        
        landmarks = HD.getLandmarks()
        
        if landmarks:
            landmarks = prepareLandmarks(landmarks)
            y_pred = GP.predict(landmarks)
            frame = handleInput(y_pred, frame)
        else:
            MC.resetMousePos()
            
        fps = str(int(1.0 / (time.time() - start_time)))

        cv2.putText(frame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        frame = cv2.resize(frame, (640, 480))
        
        cv2.imshow('Virtual Mouse', frame)

        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break
        
except Exception as e:
    print(f'Error: {e}')
    
finally:
    cap.release()
    cv2.destroyAllWindows()
    capture_thread.join()