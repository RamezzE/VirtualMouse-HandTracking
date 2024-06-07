import cv2
import numpy as np

class KalmanFilter1D:
    def __init__(self, process_noise=1e-3, measurement_noise=1e-1):
        self.kf = cv2.KalmanFilter(2, 1)
        self.kf.transitionMatrix = np.array([[1, 1], [0, 1]], np.float32)
        self.kf.measurementMatrix = np.array([[1, 0]], np.float32)
        self.kf.processNoiseCov = np.eye(2, dtype=np.float32) * process_noise
        self.kf.measurementNoiseCov = np.eye(1, dtype=np.float32) * measurement_noise
        self.kf.errorCovPost = np.eye(2, dtype=np.float32)
        self.kf.statePost = np.zeros((2, 1), np.float32)

    def update(self, measurement):
        self.kf.predict()
        estimate = self.kf.correct(np.array([[measurement]], dtype=np.float32))
        
        return estimate[0][0].flatten()
        
    def reset(self):
            self.__init__()
            