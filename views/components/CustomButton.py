from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.properties import StringProperty, ObjectProperty, ColorProperty
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage

Builder.load_file('views/components/CustomButton.kv')

class CustomButton(ButtonBehavior, Label):
    normal_image = StringProperty()
    pressed_image = StringProperty()
    
    normal_texture = ObjectProperty()
    pressed_texture = ObjectProperty()
    current_texture = ObjectProperty()
    
    normal_text_color = ColorProperty([0, 0, 0, 1]) 
    pressed_text_color = ColorProperty([1, 0, 0, 1])

    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.bind(
            normal_image=self.update_textures,
            pressed_image=self.update_textures,
            state=self.update_state_dependencies,
            normal_text_color=self.update_state_dependencies,
            pressed_text_color=self.update_state_dependencies
        )    

    def update_textures(self, *args):
        if self.normal_image:
            self.normal_texture = CoreImage(self.normal_image).texture
        if self.pressed_image:
            self.pressed_texture = CoreImage(self.pressed_image).texture
        self.update_state_dependencies()

    def update_state_dependencies(self, *args):
        if self.state == 'normal':
            self.current_texture = self.normal_texture
            self.color = self.normal_text_color
        else:
            self.current_texture = self.pressed_texture if self.pressed_texture else self.normal_texture
            self.color = self.pressed_text_color