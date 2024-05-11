import cv2
from handDetector import HandDetector
import pandas as pd

HD = HandDetector()

cap = cv2.VideoCapture(0)

collected_landmarks = []
labels = []
labelName = ""

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
            
    landmarks = HD.getLandmarks()
    
    frame_landmarks = []
    
    if landmarks:
        for landmark in landmarks:
            frame_landmarks.append(landmark.x)
            frame_landmarks.append(landmark.y)
            frame_landmarks.append(landmark.z)
            
        # if not empty
        if frame_landmarks != []:
            collected_landmarks.append(frame_landmarks)
            labels.append(labelName)
            
    cv2.imshow('Collecting Data', frame)
    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break
    
    
X = pd.DataFrame(collected_landmarks)
y = pd.DataFrame(labels)

df = pd.concat([X, y], axis = 1)

csvFile = f"Collected Dataset/{labelName}.csv"
df.to_csv(csvFile, index = False)

cap.release()
cv2.destroyAllWindows()