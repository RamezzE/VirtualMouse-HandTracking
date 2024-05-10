import cv2
from hand_detector import Hand_Detector
from mouse_controller import Mouse_Controller
import pyautogui

HD = Hand_Detector()
MC = Mouse_Controller(pyautogui.size())

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
    frame = HD.highlightFingers(img = frame, fingers = [HD.THUMB, HD.INDEX, HD.MIDDLE])

    if HD.isFingerOnlyUp(HD.INDEX):
        MC.moveMouse(pos = HD.getFingerPosition(HD.INDEX)[2:], sensitivity = 1.75)
        
    distance, frame = HD.getDistance(HD.INDEX, HD.THUMB, img = frame, draw = True)
    
    if distance is not None and distance < 25:
        MC.clickMouse() 

    cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break  

cap.release()
cv2.destroyAllWindows()