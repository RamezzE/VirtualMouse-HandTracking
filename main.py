import cv2
from handDetector import HandDetector
from mouseController import MouseController
import pyautogui
import numpy as np
from tensorflow.keras.models import load_model
import time

# get screensize without pyautogui
# i want to get it automatically from the screen
# to be able to use it across any screen

screenSize = pyautogui.size()

HD = HandDetector()
MC = MouseController(screenSize)

cap = cv2.VideoCapture(0)

arr = ['idle', 'left_click', 'right_click', 'move_mouse', 'press_and_hold_left_click', 'pinch', 'scroll', 'double_click']

IDLE = 0
LEFT_CLICK = 1
RIGHT_CLICK = 2
MOVE_MOUSE = 3
PRESS_AND_HOLD_LEFT_CLICK = 4
PINCH = 5
SCROLL = 6
DOUBLE_LEFT_CLICK = 7

tf_model = load_model('model/model2.keras')

def preprocess(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    return [(val - min_val) / (max_val - min_val) for val in arr]

def prepareLandmarks(landmarks):
    x_values = []
    y_values = []
    z_values = []
    X = []
    
    for landmark in landmarks:
        x_values.append(landmark.x)
        y_values.append(landmark.y)
        z_values.append(landmark.z)
        
    if x_values != [] and y_values != [] and z_values != []:
        x_values_normalized = preprocess(x_values)
        y_values_normalized = preprocess(y_values)
        z_values_normalized = preprocess(z_values)
        
        for x, y, z in zip(x_values_normalized, y_values_normalized, z_values_normalized):
            X.append(x)
            X.append(y)
            X.append(z)
            
    X = np.array(X)
    X = X.reshape(1, -1)
    
    return X

def handleInput(prediction, frame):
    print(arr[prediction])
    
    if prediction == IDLE:
        MC.handleMousePress(False)
        MC.resetClick()
        return frame
    
    if prediction == LEFT_CLICK:
        # if (HD.isDistanceWithin(HD.INDEX, HD.MIDDLE, 35)):
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
        
    MC.moveMouse(HD.getFingerPosition(HD.INDEX), frame.shape)
    return frame

while True:
    start_time = time.time()
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
    
    landmarks = HD.getLandmarks()
    
    if landmarks:
        landmarks = prepareLandmarks(landmarks)
        y_pred_probabilities = tf_model(landmarks)
        y_pred_index = np.argmax(y_pred_probabilities, axis=1)
        frame = handleInput(y_pred_index[0], frame)
    
    cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)
    
    # print('FPS: ', int(1 / (time.time() - start_time)))
    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()