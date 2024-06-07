from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.image import Image

class GestureRow(BoxLayout):
    settings = ObjectProperty()
    alternate_background = BooleanProperty(False)
    image_source = StringProperty()