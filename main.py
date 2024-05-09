import cv2
from hand_detector import Hand_Detector

HD = Hand_Detector()

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    
    HD.process(frame)
    
    frame = HD.drawHands(img = frame, fingerIdsToDraw = [4,8,20], drawConnections = True)
    
    cv2.imshow('Virtual Mouse', frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break  

cap.release()
cv2.destroyAllWindows()