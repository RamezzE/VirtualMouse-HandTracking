from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior

class CustomButton(ButtonBehavior, Label):
    border_radius = NumericProperty(10)
    background_color = ListProperty([0, 0, 0, 1])

    def __init__(self, font_name, text="Button", text_color=(1, 1, 1, 1),
                 default_color=[0, 0, 0, 1], pressed_color=[1, 0, 0, 1], font_size=48, border_radius = 10, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        
        self.text = text
        self.color = text_color
        self.font_name = font_name
        self.font_size = font_size

        self.default_color = default_color
        self.pressed_color = pressed_color
        self.background_color = self.default_color
        self.border_radius = border_radius
        
        # Set up transparent backgrounds for different button states
        self.background_normal = ""
        self.background_down = ""
        
        # Initialize the canvas
        with self.canvas.before:
            self.color_instruction = Color(rgba=self.background_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])
        
        # Bind necessary properties
        self.bind(pos=self.update_rect, size=self.update_rect, background_color=self.update_background_color)
        self.bind(texture_size=self.adjust_size) 
        
        self.bind(on_press=self.on_button_press)
        self.bind(on_release=self.on_button_release)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_background_color(self, *args):
        self.color_instruction.rgba = self.background_color

    def on_button_press(self, *args):
        self.background_color = self.pressed_color

    def on_button_release(self, *args):
        self.background_color = self.default_color

    def adjust_size(self, *args):
        # Adjust the size of the button based on texture size plus padding
        padding_x = 30  # Sufficient horizontal padding
        padding_y = 20  # Sufficient vertical padding
        self.size = (self.texture_size[0] + padding_x, self.texture_size[1] + padding_y)
        self.rect.size = self.size