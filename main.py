import cv2
from handDetector import HandDetector
from mouseController import MouseController
import pyautogui
import threading

HD = HandDetector(pyautogui.size())
MC = MouseController(pyautogui.size())

cap = cv2.VideoCapture(0)
            
mouseLongPress_thread = threading.Thread(target = MC.handleMousePressThread, args = (HD.isFistClosed))
mouseLongPress_thread.daemon = True 
mouseLongPress_thread.start()

while True:
    _, frame = cap.read()
    
    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
    frame = HD.highlightFingers(img = frame, fingers = [HD.THUMB, HD.INDEX, HD.MIDDLE])
        
    distance, frame = HD.getDistance(HD.INDEX, HD.THUMB, img = frame, draw = True)
    
    if not MC.handleMousePress(HD.isFistClosed()):
        if distance is not None and distance < 25:
            MC.clickMouse()
    
    if HD.isFingerOnlyUp(HD.INDEX):
        MC.moveMouse(pos = HD.getFingerPosition(HD.INDEX)[2:], sensitivity = 1.75) 
    elif HD.isFistClosed():
        MC.moveMouse(pos = HD.getFingerPosition(HD.INDEX)[2:], sensitivity = 1.25) 
    
    cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()