import threading
from models.SettingsModel import SettingsModel
from views.components.CustomDropdown import CustomDropdown

class SettingsPresenter:
    def __init__(self, view):
        self.view = view
        self.model = SettingsModel()
        self.view.set_presenter(self)
        
        self.load_initial_settings()
        self.view.draw_settings()

    def load_initial_settings(self):
        self.view.set_fonts(self.model.get_fonts())
        self.view.set_icons(self.model.get_icons())
        self.view.set_gesture_options(self.model.get_actions())
        self.view.set_mappings(self.model.get_mappings())
        self.view.set_detection_confidence(self.model.get_detection_confidence())
        self.view.set_tracking_confidence(self.model.get_tracking_confidence())
        self.view.set_detection_responsiveness(self.model.get_detection_responsiveness())
        
        selected_camera = self.model.get_last_used_camera()
        show_fps = self.model.get_show_fps_setting()
        available_camera_indices = self.model.get_available_cameras()
        
        camera_options = [f'Camera {i+1}' for i in available_camera_indices]
        if len(camera_options) <= 0:
            camera_options = ['No Camera Found']
            selected_camera = 'No Camera Found'
        elif selected_camera not in camera_options:
            selected_camera = camera_options[0]
        
        self.view.set_camera_options(camera_options)
        self.view.set_selected_camera(selected_camera)
        self.view.set_show_fps(show_fps)
        
        self.numeric_gesture_options = {v: k for k, v in enumerate(self.view.gesture_options)}

    def get_new_gesture_mappings(self):
        dropdowns = self.get_dropdowns(self.view.ids['gestures_table'])
        dropdowns.reverse()
        new_mappings = [self.numeric_gesture_options[dropdown.selected] for dropdown in dropdowns]

        mappings_to_change = [
            [i, new_mappings[i]+1] for i in range(len(self.view.mappings)) if self.view.mappings[i]-1 != new_mappings[i]
        ]
        return mappings_to_change

    def get_dropdowns(self, widget):
        custom_dropdowns = [child for child in widget.children if isinstance(child, CustomDropdown)]
        for child in widget.children:
            custom_dropdowns.extend(self.get_dropdowns(child))
        return custom_dropdowns

    def update_general_settings(self):
        detection_confidence = float(self.view.sliders[1].value) / 100
        tracking_confidence = float(self.view.sliders[0].value) / 100
        detection_responsiveness = self.get_dropdowns(self.view.ids.detection_settings)
        detection_responsiveness = detection_responsiveness[0].selected
        detection_responsiveness = 1 if detection_responsiveness == 'Instant' else 3 if detection_responsiveness == 'Fast' else 5 if detection_responsiveness == 'Normal' else 7

        if detection_confidence != self.view.detection_confidence:
            self.model.update_detection_confidence(detection_confidence)
            self.view.detection_confidence = detection_confidence

        if tracking_confidence != self.view.tracking_confidence:
            self.model.update_tracking_confidence(tracking_confidence)
            self.view.tracking_confidence = tracking_confidence
            
        if detection_responsiveness != self.view.detection_responsiveness:
            self.model.update_detection_responsiveness(detection_responsiveness)
            self.view.detection_responsiveness = detection_responsiveness
            
    def update_gesture_mappings(self):
        indices_to_change = self.get_new_gesture_mappings()

        for gesture_id, action_id in indices_to_change:
            self.model.update_gesture_mappings(gesture_id, action_id)

    def update_settings(self):
        self.view.manager.get_screen('camera').ids.GCP.presenter.saving_settings = True
        self.update_general_settings()
        self.update_gesture_mappings()
        self.view.manager.get_screen('camera').ids.GCP.presenter.update_settings(self.view.detection_confidence, self.view.tracking_confidence, self.view.detection_responsiveness)
        self.view.manager.get_screen('camera').ids.GCP.presenter.saving_settings = False

    def to_camera_screen(self):
        self.view.switch_to_camera_screen()
        threading.Thread(target=self.update_settings).start()
