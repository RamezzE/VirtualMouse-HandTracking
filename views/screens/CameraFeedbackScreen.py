from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from views.components import GestureDetectionView, CustomButton, LogsRow

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder

from presenters import CameraFeedbackPresenter
class CameraFeedbackScreen(Screen):
        
    Builder.load_file('kv/CameraFeedbackScreen.kv')

    def __init__(self, **kwargs):
        super(CameraFeedbackScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        
        self.presenter = CameraFeedbackPresenter(self)
        
        self.log_rows = []
        
        self.bind(size = self.resize)
        
    def add_log(self, prediction_no, action_name, max_logs = 10):
        
        if len(self.log_rows) > max_logs:
            self.ids['logs_table'].remove_widget(self.log_rows.pop(0))
            
        self.log_rows.append(LogsRow(prediction_no = prediction_no, action_name = action_name))
        self.ids['logs_table'].add_widget(self.log_rows[-1])
        self.ids['logs_scroll'].scroll_y = 0  
        
    def set_log_callback(self, callback):
        self.ids['GCP'].set_log_callback(callback)
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def switch_screen(self, screen_name, direction):
        self.manager.transition.direction = direction
        self.manager.current = screen_name
        
    def start_camera(self):
        self.ids['GCP'].start_camera()
        
    def stop_camera(self):
        self.ids['GCP'].stop_camera()
        
    def open_github(self):
        import webbrowser
        webbrowser.open('https://github.com/RamezzE/VirtualMouse-HandTracking')
        
    def on_stop(self):
        self.stop_camera()