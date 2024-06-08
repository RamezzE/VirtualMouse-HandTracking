from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.label import Label
from kivy.uix.slider import Slider

class SliderRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty("Slider Value:")
    alternate_background = BooleanProperty(False)
    min = NumericProperty(0)
    max = NumericProperty(100)
    value = NumericProperty(0)
    step = NumericProperty(1)
    
    def __init__(self, **kwargs):
        super(SliderRow, self).__init__(**kwargs)
        self.ids.slider.value = self.value
    
    def on_value(self, instance = None, value = None):
        try:
            self.value = int(self.ids.slider.value)
        except:
            pass       