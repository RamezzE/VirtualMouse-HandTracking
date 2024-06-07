from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.lang import Builder

Builder.load_file('kv/components/settings/SettingsComponents.kv')

class ChooseSettingButton(Button):
    settings = ObjectProperty()
    
class DropdownRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    options = ListProperty()
    alternate_background = BooleanProperty(False)
    selected = StringProperty()
    
class SliderRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty("Slider Value:")
    alternate_background = BooleanProperty(False)
    min = NumericProperty(0)
    max = NumericProperty(100)
    value = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(SliderRow, self).__init__(**kwargs)
        self.ids.slider.value = self.value
    
    def on_value(self, instance = None, value = None):
        try:
            self.value = int(self.ids.slider.value)
        except:
            pass       
            
class OnOffRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    alternate_background = BooleanProperty(False)
    
class GestureRow(BoxLayout):
    settings = ObjectProperty()
    alternate_background = BooleanProperty(False)
    image_source = StringProperty()