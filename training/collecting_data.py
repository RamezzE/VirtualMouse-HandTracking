import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.HandDetector import HandDetector

import pandas as pd
import numpy as np

HD = HandDetector()

cap = cv2.VideoCapture(0)

collected_landmarks = []
labels = []
label_name = "gesture_name"

def prepareLandmarks(landmarks):
    x_values = np.array([landmark.x for landmark in landmarks])
    y_values = np.array([landmark.y for landmark in landmarks])
    z_values = np.array([landmark.z for landmark in landmarks])

    if x_values.size > 0 and y_values.size > 0 and z_values.size > 0:
        x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
        y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())
        z_values = (z_values - z_values.min()) / (z_values.max() - z_values.min())

    arr = np.concatenate((x_values, y_values, z_values))
    return arr.reshape(1, -1)

def flip_landmarks(landmarks, axis='horizontal'):
    length = len(landmarks) // 3
    x_values = landmarks[:length]
    y_values = landmarks[length:2*length]
    z_values = landmarks[2*length:]

    if axis == 'horizontal':
        x_values = 1 - x_values
    elif axis == 'vertical':
        y_values = 1 - y_values
    elif axis == 'both':
        x_values = 1 - x_values
        y_values = 1 - y_values

    return np.concatenate((x_values, y_values, z_values)).reshape(1, -1)

def add_noise(landmarks, noise_level=0.01):
    noise = np.random.normal(0, noise_level, landmarks.shape)
    noisy_landmarks = landmarks + noise
    noisy_landmarks = np.clip(noisy_landmarks, 0, 1)
    return noisy_landmarks

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.find_hands(img=frame, draw_connections=True)
            
    landmarks = HD.get_landmarks()
        
    if landmarks:
        normalized_landmarks = prepareLandmarks(landmarks)
        
        # Augmentations
        H_flipped_landmarks = flip_landmarks(normalized_landmarks, axis='horizontal')
        V_flipped_landmarks = flip_landmarks(normalized_landmarks, axis='vertical')
        HV_flipped_landmarks = flip_landmarks(normalized_landmarks, axis='both')
        noisy_landmarks = add_noise(normalized_landmarks)
        
        collected_landmarks.extend([normalized_landmarks, H_flipped_landmarks, V_flipped_landmarks, HV_flipped_landmarks, noisy_landmarks])
        # collected_landmarks.extend([normalized_landmarks, H_flipped_landmarks, noisy_landmarks])
        # labels.extend([label_name] * 3)
        labels.extend([label_name] * 5)
        
    cv2.imshow('Collecting Data', frame)
    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break

col_names = []

for i in range(21):
    col_names.append(f'x{i+1}')
for i in range(21):    
    col_names.append(f'y{i+1}')
for i in range(21):
    col_names.append(f'z{i+1}')
    
X = pd.DataFrame(np.vstack(collected_landmarks), columns=col_names)
y = pd.DataFrame(labels, columns=['label'])

df = pd.concat([X, y], axis=1)

csv_path = f"training/Collected Dataset/{label_name}.csv"
df.to_csv(csv_path, index=False)

cap.release()
cv2.destroyAllWindows()
