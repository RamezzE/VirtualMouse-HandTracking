import numpy as np

class GesturePredictor:
                
    def __init__(self, model, buffer_size = 5, is_tf = False, pca = None):
        self.model = model
        self.is_tf = is_tf
        self.buffer_size = buffer_size
        self.pca = pca
        self.prediction_buffer = []
        
    def predict(self, landmarks):
                
        landmarks = self._prepare_landmarks(landmarks)
        
        if self.pca is not None:
            landmarks = self.pca.transform(landmarks)
        
        if self.is_tf:
            prediction = self.model(landmarks)
            
            prediction = np.argmax(prediction)
        else:
            prediction = (self.model.predict(landmarks))[0]
            
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
        z_values = np.array([landmark.z for landmark in landmarks])

        if x_values.size > 0 and y_values.size > 0:
            x_values = (x_values - x_values.min()) / (x_values.max() - x_values.min())
            y_values = (y_values - y_values.min()) / (y_values.max() - y_values.min())
            z_values = (z_values - z_values.min()) / (z_values.max() - z_values.min())

        arr = np.concatenate((x_values, y_values, z_values))
        return arr.reshape(1, -1)
    
    def set_buffer_size(self, buffer_size):
        self.prediction_buffer.clear()
        self.buffer_size = buffer_size
        print(f'Buffer size set to {buffer_size}')