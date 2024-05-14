import cv2
from handDetector import HandDetector
import pandas as pd

HD = HandDetector()

cap = cv2.VideoCapture(0)

collected_landmarks = []
labels = []
labelName = "name_of_gesture"

def preproceess(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    return [(val - min_val) / (max_val - min_val) for val in arr]


while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
            
    landmarks = HD.getLandmarks()
        
    if landmarks:
        x_values = []
        y_values = []
        z_values = []
        
        for landmark in landmarks:
            x_values.append(landmark.x)
            y_values.append(landmark.y)
            z_values.append(landmark.z)
            
        # if not empty
        if x_values != [] and y_values != [] and z_values != []:
            x_values_normalized = preproceess(x_values)
            y_values_normalized = preproceess(y_values)
            z_values_normalized = preproceess(z_values)
            
            # Flip the x and y values
            x_values_normalized_flipped = [1 - val for val in x_values_normalized]
            y_values_normalized_flipped = [1 - val for val in y_values_normalized]

            normalized_landmarks = [coord for coords in zip(x_values_normalized, y_values_normalized, z_values_normalized) for coord in coords]
            H_flipped_landmarks = [coord for coords in zip(x_values_normalized_flipped, y_values_normalized, z_values_normalized) for coord in coords]
            V_flipped_landmarks = [coord for coords in zip(x_values_normalized, y_values_normalized_flipped, z_values_normalized) for coord in coords]
            HV_flipped_landmarks = [coord for coords in zip(x_values_normalized_flipped, y_values_normalized_flipped, z_values_normalized) for coord in coords]
            
            collected_landmarks.extend([normalized_landmarks, H_flipped_landmarks, V_flipped_landmarks, HV_flipped_landmarks])
            labels.extend([labelName] * 4)
        
        
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