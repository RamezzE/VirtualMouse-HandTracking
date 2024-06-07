from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty, BooleanProperty, ColorProperty
from kivy.lang import Builder
import yaml

class CustomDropdown(FloatLayout):
    selected = StringProperty()
    font_name = StringProperty()
    font_size = NumericProperty(20)
    
    options = ListProperty([])
    text_color = ColorProperty([1, 1, 1, 1])
    
    button_width = NumericProperty(50)
    button_height = NumericProperty(50)
    
    options_height = NumericProperty()
    
    background_color = ColorProperty([0, 0, 0, 1])
    alt_background_color = ColorProperty([0, 0, 0, 1])
    
    image_path = StringProperty()
    
    dropdown = ObjectProperty()
    
    dropdown_open = BooleanProperty(False)
    
    _i = None
    
    with open('paths.yaml', 'r') as f:
        paths = yaml.safe_load(f)

    icons = paths['assets']['icons']
    
    Builder.load_file('views/components/CustomDropdown.kv')
    
    def __init__(self, **kwargs):
        super(CustomDropdown, self).__init__(**kwargs)
        
        self.dropdown = DropDown()
        
        if self.options_height == 0:
            self.options_height = self.button_height
        
        self.bind(options=self._update_options)
        
        self.dropdown.bind(
            on_select=lambda instance, x: setattr(self, 'selected', x),
            on_dismiss=lambda instance: setattr(self, 'dropdown_open', False)
        )
        
        self.optionButtons = []           
        self.define_options(self.options)
        
    def get_selected(self):
        return self.selected
    
    def define_options(self, options):
        self.options = options
        for option in options:
            btn = self._create_option(option)
            self.dropdown.add_widget(btn)
        
    def get_options(self):
        return self.options
    
    def clear_options(self):
        self.options = []
        self.dropdown.clear_widgets()
    
    def _open_dropdown(self):
        self.dropdown.open(self)
        self.dropdown_open = True
        
    def _create_option(self, option):
                
        if self._i is None:
            self._i = 0
            
        if self._i % 2 == 0:
            btn = OptionButton(text=option, dropdown=self, alternate_background = False)
        else:
            btn = OptionButton(text=option, dropdown=self, alternate_background = True)
        
        if self.font_name:
            btn.font_name = self.font_name
        
        self._i += 1
        
        self.optionButtons.append(btn)
        return btn
        
    def _update_options(self, instance, value):
        self.define_options(value)
        
class OptionButton(Button):
    dropdown = ObjectProperty()
    alternate_background = BooleanProperty(False)
