import numpy as np

class GesturePredictor:
    def __init__(self, model, buffer_size = 5):
        self.model = model
        self.buffer_size = buffer_size
        self.prediction_buffer = []

    def predict(self, landmarks):
        prediction = (self.model.predict(landmarks))[0]

        self.prediction_buffer.append(prediction)
        
        if len(self.prediction_buffer) > self.buffer_size:
            self.prediction_buffer.pop(0)
        
        return max(set(self.prediction_buffer), key=self.prediction_buffer.count)