from kivy.uix.actionbar import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.accordion import ListProperty
from kivy.uix.actionbar import ColorProperty
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.button import Button

class CustomDropDown(FloatLayout):
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
    
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        
        self.dropdown = DropDown()
        # self.dropdown.open = self.custom_open
        
        if self.options_height == 0:
            self.options_height = self.button_height
        
        self.bind(text_color=self._update_text_color)
        self.bind(font_name=self._update_font_name)
        self.bind(options=self._update_options)
        
        self.bind(button_height=self._update_button_height)
        self.bind(options_height=self._update_button_height)
        self.bind(button_width=self._update_button_width)
        
        self.bind(background_color=self._update_background_color)
        self.bind(alt_background_color=self._update_background_color)
        
        self.bind(font_size=self._update_options_font_size)
                
        self.selectedBtn = self._create_option(self.selected, False)
        
        self.selectedBtn.bind(on_release=self.dropdown.open)
        self.bind(selected=self.selectedBtn.setter('text'))

        self.add_widget(self.selectedBtn)
        self.define_options(self.options)
        
        self.optionButtons = []
        self.optionButtons.append(self.selectedBtn)
        
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.selectedBtn, 'text', x))
       
    def custom_open(self, widget):
        self.dropdown.width = widget.width

        DropDown.open(self.dropdown, widget)
        self.dropdown.container.pos = (widget.x, widget.y - self.dropdown.container.height)

        
    def define_options(self, options):
        self.options = options
        for option in options:
            btn = self._create_option(option)
            self.dropdown.add_widget(btn)
    
    def clear_options(self):
        self.options = []
        self.dropdown.clear_widgets()
        
    def get_options(self):
        return self.options
        
    def _create_option(self, option, bool = True):
        btn = Button(
            text=option,
            color=self.text_color,
            size_hint = (None, None),
            font_size = self.font_size,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=self.background_color,
            background_normal='',
            background_down='',
        )
        
        if self.font_name:
            btn.font_name = self.font_name

        if not bool:
            return btn
        
        btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        
        self.optionButtons.append(btn)
        
        return btn

    def _update_button_width(self, instance, value):
        for btn in self.optionButtons:
            btn.width = value
            
    def _update_button_height(self, instance, value):
        for btn in self.optionButtons:
            btn.height = self.options_height
            
        self.selectedBtn.height = self.button_height
        
    def _update_text_color(self, instance, value):
        for btn in self.optionButtons:
            btn.normal_text_color = value
            btn.color = value
        
    def _update_options(self, instance, value):
        self.define_options(value)
        
    def _update_font_name(self, instance, value):
        for btn in self.optionButtons:
            btn.font_name = value
            
    def _update_options_font_size(self, instance, value):
        for btn in self.optionButtons:
            btn.font_size = value

        
    def _update_background_color(self, instance, value):
        i = 0
        for btn in self.optionButtons:
            btn.background_color = self.background_color if i % 2 == 0 else self.alt_background_color
            i += 1
    
    def get_selected(self):
        return self.selectedBtn.text
    