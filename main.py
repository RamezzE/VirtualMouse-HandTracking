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

arr = ['idle', 'left_click', 'right_click', 'move_mouse', 'press_and_hold_left_click', 'scroll']

IDLE = 0
LEFT_CLICK = 1
RIGHT_CLICK = 2
MOVE_MOUSE = 3
PRESS_AND_HOLD_LEFT_CLICK = 4
SCROLL = 5

tf_model = load_model('model/model2.keras')

def prepareLandmarks(landmarks):
    x_values = []
    y_values = []
    X = []
    
    for landmark in landmarks:
        x_values.append(landmark.x)
        y_values.append(landmark.y)
        
    if x_values != [] and y_values != []:
        min_x = min(x_values)
        max_x = max(x_values)
        
        min_y = min(y_values)
        max_y = max(y_values)

        x_values_normalized = [(x - min_x) / (max_x - min_x) for x in x_values]
        y_values_normalized = [(y - min_y) / (max_y - min_y) for y in y_values]
        
        for x, y in zip(x_values_normalized, y_values_normalized):
            X.append(x)
            X.append(y)
            
    X = np.array(X)
    X = X.reshape(1, -1)
    
    return X

def handleInput(prediction, frame):
    # print(arr[prediction])
    
    if prediction == IDLE:
        MC.handleMousePress(False)
        MC.resetClick()
        return frame
    
    if prediction == LEFT_CLICK or prediction == RIGHT_CLICK:
        left_click = HD.isDistanceWithin(HD.INDEX, HD.THUMB)
        right_click = HD.isDistanceWithin(HD.MIDDLE, HD.THUMB)
        
        if left_click == right_click:
            return frame
        
        if left_click:
            MC.clickMouse(button = 'left')
            MC.resetClick(button = 'right')
            return HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.THUMB])
            
        if right_click:
            MC.clickMouse(button = 'right') 
            MC.resetClick(button = 'left')    
            return HD.highlightFingers(img = frame, fingers = [HD.MIDDLE, HD.THUMB])
            
    if prediction == SCROLL:
        frame = HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE])
        MC.handleMousePress(False)
        MC.resetClick()
        MC.handleScroll()
        return frame
        
    if prediction == MOVE_MOUSE:
        # ADD HD Validation
        MC.handleMousePress(False)
        MC.resetClick()
        frame = HD.highlightFingers(img = frame, fingers = [HD.INDEX, HD.MIDDLE])
    
    elif prediction == PRESS_AND_HOLD_LEFT_CLICK:
        MC.handleMousePress(True)
        MC.resetClick(button = 'left')
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
    
    # cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)
    
    print('FPS: ', int(1 / (time.time() - start_time)))
    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()