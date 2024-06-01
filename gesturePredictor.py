import numpy as np
import sqlite3
from db import Database

class GesturePredictor:
    
    IDLE = 0
    LEFT_CLICK = 1
    RIGHT_CLICK = 2
    MOVE_MOUSE = 3
    DRAG = 4
    PINCH = 5
    SCROLL = 6
    DOUBLE_LEFT_CLICK = 7
    
    def __init__(self, tensorflow_model, buffer_size = 5):
        self.model = tensorflow_model
        self.buffer_size = buffer_size
        self.prediction_buffer = []
        
        self.db = Database('db/actions.db', 'db/schema.sql')
        
        self.actions = self.db.getActionNames()
        self.mappings = self.db.getMappings()

    def predict(self, landmarks):
        prediction = self.model(landmarks)
        
        prediction = np.argmax(prediction)

        self.prediction_buffer.append(prediction)
        
        if len(self.prediction_buffer) > self.buffer_size:
            self.prediction_buffer.pop(0)
        
        return max(set(self.prediction_buffer), key=self.prediction_buffer.count)
    
    def getAction(self, prediction):
        for mapping in self.mappings:
            if mapping[0] == prediction:
                return self.actions[mapping[1]-1], mapping[1]-1
        