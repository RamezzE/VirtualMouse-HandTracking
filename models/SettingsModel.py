from kivy.app import App
import numpy as np
from presenters import CameraPresenter as Camera

class SettingsModel:
    def __init__(self):
        self.paths = App.get_running_app().paths

        self.db = App.get_running_app().db
        
    def get_fonts(self):
        return self.paths['assets']['fonts']

    def get_icons(self):
        return self.paths['assets']['icons']

    def get_actions(self):
        return (np.array(self.db.get('Actions', columns_to_select='name'))).reshape(-1)

    def get_mappings(self):
        return np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)

    def get_last_used_camera(self):
        return self.db.get('CameraSettings', columns_to_select=['value'], name='Camera')[0]

    def get_show_fps_setting(self):
        return self.db.get('CameraSettings', columns_to_select=['value'], name='Show FPS')[0]

    def get_detection_confidence(self):
        return float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Confidence')[0])

    def get_tracking_confidence(self):
        return float(self.db.get('DetectionSettings', columns_to_select=['value'], name='Tracking Confidence')[0])

    def get_detection_responsiveness(self):
        return int(self.db.get('DetectionSettings', columns_to_select=['value'], name='Detection Responsiveness')[0])
    
    def update_detection_confidence(self, value):
        self.db.update('DetectionSettings', {'value': value}, name='Detection Confidence')

    def update_tracking_confidence(self, value):
        self.db.update('DetectionSettings', {'value': value}, name='Tracking Confidence')

    def update_gesture_mappings(self, gesture_id, action_id):
        self.db.update('Mappings', {'action_id': action_id}, gesture_id=gesture_id)
        
    def update_detection_responsiveness(self, value):
        self.db.update('DetectionSettings', {'value': value}, name='Detection Responsiveness')
        
    def get_available_cameras(self):
        return np.array(Camera.get_available_cameras(5))
