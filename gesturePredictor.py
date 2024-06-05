import numpy as np

class GesturePredictor:
     
    IDLE = 0
    MOVE_MOUSE = 1
    LEFT_CLICK = 2
    DOUBLE_CLICK = 3
    DRAG = 4
    RIGHT_CLICK = 5
    SCROLL_UP = 6
    SCROLL_DOWN = 7
    ZOOM = 8
    TOGGLE_RELATIVE_MOUSE = 9
                
    def __init__(self, tensorflow_model, buffer_size = 5):
        self.model = tensorflow_model
        self.buffer_size = buffer_size
        self.prediction_buffer = []
        
    def predict(self, landmarks):
                
        landmarks = self._prepareLandmarks(landmarks)
        
        prediction = self.model(landmarks)
        
        prediction = np.argmax(prediction)

        self.prediction_buffer.append(prediction)
        
        if len(self.prediction_buffer) > self.buffer_size:
            self.prediction_buffer.pop(0)
        
        return max(set(self.prediction_buffer), key=self.prediction_buffer.count)
        
    def _prepareLandmarks(self, landmarks):
        x_values = np.array([landmark.x for landmark in landmarks])
        y_values = np.array([landmark.y for landmark in landmarks])

        if x_values.size > 0 and y_values.size > 0:
            x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
            y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

        arr = np.concatenate((x_values, y_values))
        return arr.reshape(1, -1)