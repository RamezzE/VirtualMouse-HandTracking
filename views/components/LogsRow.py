from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
from datetime import datetime

class LogsRow(BoxLayout):
    current_time = StringProperty()
    prediction_no = NumericProperty(0)
    action_name = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_time = str(datetime.now().strftime('%H:%M:%S'))
    