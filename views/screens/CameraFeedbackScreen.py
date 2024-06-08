from kivy.uix.accordion import NumericProperty
from kivy.uix.accordion import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from views.components.GestureDetectionView import GestureDetectionView 
from views.components.CustomButton import CustomButton

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder

from presenters.CameraFeedbackPresenter import CameraFeedbackPresenter
from views.components import LogsRow
class CameraFeedbackScreen(Screen):
        
    Builder.load_file('views/screens/CameraFeedbackScreen.kv')

    def __init__(self, **kwargs):
        super(CameraFeedbackScreen, self).__init__(**kwargs)
        
        self.size = Window.size
        self.pos = Window._pos
        
        CameraFeedbackPresenter(self)
        
        self.log_rows = []
        
        self.bind(size = self.resize)   
        
    def add_log(self, prediction_no, action_name):
        
        if len(self.log_rows) > 10:
            self.ids.logs_table.remove_widget(self.log_rows.pop(0))
            
        self.log_rows.append(LogsRow(prediction_no = prediction_no, action_name = action_name))
        self.ids.logs_table.add_widget(self.log_rows[-1])
        self.ids.logs_scroll.scroll_y = 0
        
    def set_presenter(self, presenter):
        self.presenter = presenter     
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def switch_to_home_screen(self):
        self.presenter.switch_to_home_screen()
        
    def switch_to_settings_screen(self):
        self.presenter.switch_to_settings_screen()
        
    def on_stop(self):
        self.presenter.on_stop()