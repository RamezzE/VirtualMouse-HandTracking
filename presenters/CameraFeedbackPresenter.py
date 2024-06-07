class CameraFeedbackPresenter:
    def __init__(self, view):
        self.view = view
        self.view.set_presenter(self)
        
    def start_camera(self):
        print('Starting camera')
        self.view.ids['GCP'].start_camera()
        
    def stop_camera(self):
        self.view.ids['GCP'].on_stop()
        
    def on_stop(self):
        self.stop_camera()
        
    def switch_to_settings_screen(self):
        self.view.manager.transition.direction = 'up'
        self.view.manager.current = 'settings'
        self.view.on_stop()
        
    def switch_to_home_screen(self):
        self.view.manager.transition.direction = 'right'
        self.view.manager.current = 'home'
        self.view.on_stop()
