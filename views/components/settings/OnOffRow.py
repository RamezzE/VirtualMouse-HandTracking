from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.label import Label

class OnOffRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    alternate_background = BooleanProperty(False)