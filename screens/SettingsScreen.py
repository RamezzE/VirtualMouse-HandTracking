from kivy.uix.accordion import BooleanProperty
from kivy.uix.accordion import ObjectProperty
from kivy.uix.actionbar import BoxLayout
from kivy.uix.accordion import NumericProperty
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button

import yaml

from components.CustomButton import CustomButton
from components.CustomDropDown import CustomDropDown


class SettingsScreen(Screen):
    
    gesture_options = ['Idle','Move Mouse','Left Click','Double Click','Drag','Right Click','Pinch','Scroll Up','Scroll Down', 'Zoom', 'Toggle Relative Mouse',]

    with open('paths.yaml', 'r') as f:
        paths = yaml.safe_load(f)
            
    fonts = paths['assets']['fonts']
    icons = paths['assets']['icons']
    
    selected = StringProperty(None)

    rowHeight = NumericProperty()
    
    gestureRowHeight = NumericProperty()
    
    Builder.load_file('kv/screens/SettingsScreen.kv')
    
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.size = Window.size
        self.pos = Window._pos
        
        self.rowHeight = self.height * 0.08
        self.gestureRowHeight = self.rowHeight * 1.5
        
        self.select('general')
                
        self.bind(size=self.resize)
        
        self.drawGestureTable()
        self.drawSettingsHeader()
        
    def drawSettingsHeader(self):
        settings_header = self.ids['settings_header']
        
        settings_header.add_widget(ChooseSettingButton(text='General', settings=self))
        settings_header.add_widget(ChooseSettingButton(text='Gestures', settings=self))
        
    def drawGestureTable(self):
        gestures_table = self.ids['gestures_table']
        
        for i in range(11):
            gesture_row = GestureRow(settings=self, alternate_background=(i % 2 == 0), image_source = self.icons['gestures'][f'gesture{i+1}'])
            gesture_row.ids['dropdown'].selected = "X"
            
            gestures_table.add_widget(gesture_row)
                
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def toCameraScreen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'camera'
        
        dropdowns = self.getDropDowns(self.ids['gestures_table']) 
        dropdowns.reverse()
        
        for dropdown in dropdowns:
            print(dropdown.get_selected())
        
    def select(self, button_id):
        selected = self.selected
        
        self.selected = button_id
        
        if selected == 'gestures':
            pass
        
    def getDropDowns(self, widget):
        custom_dropdowns = []
        if isinstance(widget, CustomDropDown):
            custom_dropdowns.append(widget)
        for child in widget.children:
            custom_dropdowns.extend(self.getDropDowns(child))
        return custom_dropdowns
        
    def updateGestureMappings(self):
        # In process
        for child in self.ids['layout'].children:
            if isinstance(child, CustomDropDown):
                print(child.selected)
        

class GestureRow(BoxLayout):
    settings = ObjectProperty()
    alternate_background = BooleanProperty(False)
    image_source = StringProperty()
    
class ChooseSettingButton(Button):
    settings = ObjectProperty()