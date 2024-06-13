import threading
from models.SettingsModel import SettingsModel
from kivy.clock import Clock

class SettingsPresenter:
    def __init__(self, view):
        self.view = view
        self.view.presenter = self
        self.model = SettingsModel()
                
        self._load_initial_settings()
        self.view.select_setting('general')
        self._start_loading_available_cameras()
        

    def _load_initial_settings(self):
        self.view.set_gesture_options(self.model.get_actions())

        self.detection_responsiveness_options = ['Instant', 'Fast', 'Normal', 'Slow']

        self.detection_confidence = self.model.get_detection_confidence()
        self.tracking_confidence = self.model.get_tracking_confidence()
        self.detection_responsiveness = self.model.get_detection_responsiveness()
        self.relative_mouse_sensitivity = self.model.get_relative_mouse_sensitivity()

        self.mappings = self.model.get_mappings()

        self.selected_camera = self.model.get_last_used_camera()
        self.numeric_gesture_options = {v: k for k, v in enumerate(self.view.gesture_options)}

    def _start_loading_available_cameras(self):
        threading.Thread(target=self._load_available_cameras).start()

    def _load_available_cameras(self):
        self.available_camera_indices = self.model.get_available_cameras()
        self._on_available_cameras_loaded()

    def _on_available_cameras_loaded(self):
        Clock.schedule_once(self.view.draw_settings, 0)
        
    def get_detection_confidence(self):
        return int(self.detection_confidence * 100)

    def get_tracking_confidence(self):
        return int(self.tracking_confidence * 100)

    def get_detection_responsiveness(self):
        return self.detection_responsiveness_options[int(self.detection_responsiveness / 2)]

    def get_relative_mouse_sensitivity(self):
        return int(self.relative_mouse_sensitivity * 100)
    
    def get_mappings(self):
        return self.mappings

    def get_relative_mouse_sensitivity(self):
        return int(self.model.get_relative_mouse_sensitivity() * 100)
    
    def get_camera_options(self):
        
        camera_options = [f'Camera {i+1}' for i in self.available_camera_indices]
        selected_camera = self.selected_camera
        
        if len(camera_options) <= 0:
            camera_options = ['No Camera Found']
            selected_camera = 'No Camera Found'
        elif selected_camera not in camera_options:
            selected_camera = camera_options[0]
        
        return camera_options, selected_camera
    
    def get_detection_responsiveness_options(self):
        return self.detection_responsiveness_options

    def _get_new_gesture_mappings(self):
        dropdowns = self.view.get_gesture_dropdowns()
    
        new_mappings = [self.numeric_gesture_options[dropdown.selected] + 1 for dropdown in dropdowns]

        mappings_to_change = [
            [i, new_mappings[i]] for i in range(len(self.mappings)) if self.mappings[i] != new_mappings[i]
        ]

        return mappings_to_change, new_mappings

    def _update_general_settings(self):
        detection_confidence = float(self.view.get_detection_confidence_slider().value) / 100
        tracking_confidence = float(self.view.get_tracking_confidence_slider().value) / 100
        relative_mouse_sensitivity = float(self.view.get_relative_mouse_sensitivity_slider().value) / 100
        
        detection_responsiveness = self.view.get_detection_dropdowns()
        
        detection_responsiveness = detection_responsiveness[0].selected
        arr = self.detection_responsiveness_options
        
        d_r = detection_responsiveness  
        detection_responsiveness = 1 if d_r == arr[0] else 3 if d_r == arr[1] else 5 if d_r == arr[2] else 7

        if detection_confidence != self.detection_confidence:
            self.model.update_detection_confidence(detection_confidence)
            self.detection_confidence = detection_confidence

        if tracking_confidence != self.tracking_confidence:
            self.model.update_tracking_confidence(tracking_confidence)
            self.tracking_confidence = tracking_confidence
            
        if relative_mouse_sensitivity != self.relative_mouse_sensitivity:
            self.model.update_relative_mouse_sensitivity(relative_mouse_sensitivity)
            self.relative_mouse_sensitivity = relative_mouse_sensitivity
            
        if detection_responsiveness != self.detection_responsiveness:
            self.model.update_detection_responsiveness(detection_responsiveness)
            self.detection_responsiveness = detection_responsiveness
            
    def _update_gesture_mappings(self):
        indices_to_change, new_mappings = self._get_new_gesture_mappings()
        self.mappings = new_mappings

        for gesture_id, action_id in indices_to_change:
            self.model.update_gesture_mappings(gesture_id, action_id)

    def update_settings(self):
        self.view.set_saving_settings(True)
        # Update gesture mappings first
        self._update_gesture_mappings()
        self._update_general_settings()
        self.view.update_gcp_settings(self.detection_confidence, self.tracking_confidence, self.detection_responsiveness, self.relative_mouse_sensitivity, self.mappings)
        self.view.set_saving_settings(False)

    def switch_to_camera_screen(self):
        self.view.switch_screen('camera', 'right')
        threading.Thread(target=self.update_settings).start()