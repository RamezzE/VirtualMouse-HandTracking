import cv2
from handDetector import HandDetector
import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('model/model2.keras')

HD = HandDetector()

 
string_to_numeric = {'idle': 0, 'left_click': 1, 'right_click' : 2, 'move_mouse': 3, 'press_and_hold_left_click': 4, 'scroll': 5}

numeric_to_string = {v: k for k, v in string_to_numeric.items()}        

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    frame = cv2.flip(frame, 1)
        
    frame = HD.findHands(img = frame, drawConnections = True)
            
    landmarks = HD.getLandmarks()
            
    if landmarks:
        # flatten the landmarks
        landmarks_array = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])
        landmarks_array = landmarks_array.reshape(1, -1)
        
        x_values = []
        y_values = []
        X = []
        
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
                X.append(x)
                X.append(y)
                
        X = np.array(X)
        X = X.reshape(1, -1)
        y_pred_probabilities = model(X)


        y_pred_index = np.argmax(y_pred_probabilities, axis=1)
        y_pred = numeric_to_string[y_pred_index[0]]
        
        print(y_pred_index, y_pred, y_pred_probabilities)
                    
    cv2.imshow('Live Testing', frame)
    key = cv2.waitKey(1)
  
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()