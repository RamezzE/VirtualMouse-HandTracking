import cv2
from handDetector import HandDetector
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model/model2.keras')

string_to_numeric = {'idle': 0, 'left_click': 1, 'right_click' : 2, 'move_mouse': 3, 'press_and_hold_left': 4, 'pinch_action' : 5, 'scroll': 6, 'double_click':7}

numeric_to_string = {value: key for key, value in string_to_numeric.items()}

HD = HandDetector()

cap = cv2.VideoCapture(0)

def preproceess(arr):
    min_val = min(arr)
    max_val = max(arr)
    
    return [(val - min_val) / (max_val - min_val) for val in arr]

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
            
    landmarks = HD.getLandmarks()
    
    X = []
        
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
            
            for x, y, z in zip(x_values_normalized, y_values_normalized, z_values_normalized):
                X.append(x)
                X.append(y)
                X.append(z)
                

        X = [coord for coords in zip(x_values_normalized, y_values_normalized, z_values_normalized) for coord in coords]
        X = np.array(X)
        X = X.reshape(1, -1)
        y_pred_probabilities = model(X)

        y_pred_index = np.argmax(y_pred_probabilities, axis=1)
        y_pred = numeric_to_string[y_pred_index[0]]
        
        print(y_pred)
                    
    cv2.imshow('Live Testing', frame)
    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()