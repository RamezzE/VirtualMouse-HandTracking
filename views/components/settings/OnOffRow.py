from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ColorProperty
from kivy.uix.label import Label

class OnOffRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    callback = ObjectProperty()
    color_on = ColorProperty([185/255, 185/255, 185/255, 1])
    color_off = ColorProperty([110/255, 110/255, 110/255, 1])
    on = BooleanProperty(True)

    alternate_background = BooleanProperty(False)
    
    def __init__(self, on = True, **kwargs):
        super(OnOffRow, self).__init__(**kwargs)
        self.on = on
        self._on_off(on)
    
    def _on_off(self, bool):
        if bool:
            if self.on:
                return
            self.on = True
            if self.callback:
                self.callback(True)
            return
        
        if not self.on:
            return
        self.on = False
        if self.callback:
            self.callback(False) 
            
    def toggle(self):
        self._on_off(not self.on)
            
    def is_on(self):
        return self.on