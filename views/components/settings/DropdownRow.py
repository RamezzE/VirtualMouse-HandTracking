from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty

from views.components import CustomDropdown

class DropdownRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    options = ListProperty()
    alternate_background = BooleanProperty(False)
    selected = StringProperty()