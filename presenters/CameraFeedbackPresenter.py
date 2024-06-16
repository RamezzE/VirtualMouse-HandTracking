class CameraFeedbackPresenter:
    def __init__(self, view):
        self.view = view
        self.view.set_log_callback(self.add_log)
        
    def add_log(self, prediction_no, action_name):
        self.view.add_log(prediction_no, action_name)
        
    def start_camera(self):
        self.view.start_camera()
        
    def stop_camera(self):
        self.view.stop_camera()
        
    def switch_to_settings_screen(self):
        self.view.switch_screen('settings', 'up')
        self.view.on_stop()