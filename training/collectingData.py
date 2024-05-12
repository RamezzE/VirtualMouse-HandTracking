import cv2
from handDetector import HandDetector
import pandas as pd

HD = HandDetector()

cap = cv2.VideoCapture(0)

collected_landmarks = []
labels = []
labelName = "idle_5"

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
            
    landmarks = HD.getLandmarks()
    
    frame_landmarks = []
    
    if landmarks:
        x_values = []
        y_values = []
        
        for landmark in landmarks:
            x_values.append(landmark.x)
            y_values.append(landmark.y)
            
        # if not empty
        if x_values != [] and y_values != []:
            min_x = min(x_values)
            max_x = max(x_values)
            
            min_y = min(y_values)
            max_y = max(y_values)

            x_values_normalized = [(x - min_x) / (max_x - min_x) for x in x_values]
            y_values_normalized = [(y - min_y) / (max_y - min_y) for y in y_values]
            
            for x, y in zip(x_values_normalized, y_values_normalized):
                frame_landmarks.append(x)
                frame_landmarks.append(y)
                
            collected_landmarks.append(frame_landmarks)
            
            labels.append(labelName)
        
        
    cv2.imshow('Collecting Data', frame)
    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break
    
    
X = pd.DataFrame(collected_landmarks)
y = pd.DataFrame(labels)

df = pd.concat([X, y], axis = 1)

csvFile = f"training/Collected Dataset/{labelName}.csv"
df.to_csv(csvFile, index = False)

cap.release()
cv2.destroyAllWindows()