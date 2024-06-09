import numpy as np

class GesturePredictor:
                
    def __init__(self, tensorflow_model, buffer_size = 5):
        self.model = tensorflow_model
        self.buffer_size = buffer_size
        self.prediction_buffer = []
        
    def predict(self, landmarks):
                
        landmarks = self._prepare_landmarks(landmarks)
        
        prediction = self.model(landmarks)
        
        prediction = np.argmax(prediction)

        self.prediction_buffer.append(prediction)
        
        if len(self.prediction_buffer) > self.buffer_size:
            self.prediction_buffer.pop(0)
        
        try:
            return max(set(self.prediction_buffer), key=self.prediction_buffer.count)
        except:
            return prediction
        
    def _prepare_landmarks(self, landmarks):
        x_values = np.array([landmark.x for landmark in landmarks])
        y_values = np.array([landmark.y for landmark in landmarks])

        if x_values.size > 0 and y_values.size > 0:
            x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
            y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())

        arr = np.concatenate((x_values, y_values))
        return arr.reshape(1, -1)
    
    def set_buffer_size(self, buffer_size):
        self.prediction_buffer.clear()
        self.buffer_size = buffer_size
        print(f'Buffer size set to {buffer_size}')