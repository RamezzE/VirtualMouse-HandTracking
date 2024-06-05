from kivy.uix.accordion import ListProperty
from kivy.uix.actionbar import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.button import Button
from kivy.clock import Clock

import yaml
import threading

from components.CustomButton import CustomButton
from components.CustomDropDown import CustomDropDown

class SettingsScreen(Screen):
    
    gesture_options = []

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
        
        self.db = App.get_running_app().db
        self.gesture_options = self.db.get_action_names()
        self.numeric_gesture_options = {v: k for k, v in enumerate(self.gesture_options)}
        self.mappings = self.db.get_mappings()
        
        self.rowHeight = self.height * 0.08
        self.gestureRowHeight = self.rowHeight * 1.5
        
        self.select('general')
                
        self.bind(size=self.resize)
        
        self.draw_settings()
        
    def draw_settings(self):
        ## Draw the settings header
        settings_header = self.ids['settings_header']
        
        settings_header.add_widget(ChooseSettingButton(text='General', settings=self))
        settings_header.add_widget(ChooseSettingButton(text='Gestures', settings=self))
        
        ## Draw the settings content
        
        ## Camera settings
        camera_settings = self.ids['camera_settings']
        camera_settings.add_widget(DropdownRow(text='Camera Resolution', settings=self, options=['1920x1080', '1280x720', '640x480'], alternate_background=True))
        camera_settings.add_widget(DropdownRow(text='Capturing Camera', settings=self, options=['Front', 'Back']))
        camera_settings.add_widget(OnOffRow(text='Camera View', settings=self, alternate_background=True))
        camera_settings.add_widget(OnOffRow(text='Show FPS', settings=self))
        
        gestures_table = self.ids['gestures_table']
        for i in range(11):
            gesture_row = GestureRow(settings=self, alternate_background=(i % 2 == 0), image_source = self.icons['gestures'][f'gesture{i+1}'])
            gesture_row.ids['dropdown'].selected = self.gesture_options[self.mappings[i][1]]
            
            gestures_table.add_widget(gesture_row)
        
        self.ids['layout'].size = self.size
                            
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def toCameraScreen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'camera'
        
        if self.are_settings_changed():
            self.manager.get_screen('camera').ids['GCP'].saving_settings = True
            threading.Thread(target=self.update_gesture_mappings).start()
        
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
        
    def update_gesture_mappings(self):
        dropdowns = self.getDropDowns(self.ids['gestures_table']) 
        dropdowns.reverse()
        
        arr = []
        
        for dropdown in dropdowns:
            arr.append(self.numeric_gesture_options[dropdown.selected])
        
        self.db.delete_mappings()
        self.db.insert_mappings(arr)
        self.mappings = self.db.get_mappings()
        self.db.is_updated = True
        
        Clock.schedule_once(self.update_thread_loaded, 0.1)
            
    def update_thread_loaded(self, dt):
        self.manager.get_screen('camera').ids['GCP'].saving_settings = False
        
    def are_settings_changed(self):
        dropdowns = self.getDropDowns(self.ids['gestures_table'])
        dropdowns.reverse()
        arr = []
        
        for dropdown in dropdowns:
            arr.append(self.numeric_gesture_options[dropdown.selected])
        
        for i, mapping in enumerate(self.mappings):
            if mapping[1] != arr[i]:
                return True
        return False
        

    
class ChooseSettingButton(Button):
    settings = ObjectProperty()
    
class DropdownRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    options = ListProperty()
    alternate_background = BooleanProperty(False)
    
class OnOffRow(BoxLayout):
    settings = ObjectProperty()
    text = StringProperty()
    alternate_background = BooleanProperty(False)
    
class GestureRow(BoxLayout):
    settings = ObjectProperty()
    alternate_background = BooleanProperty(False)
    image_source = StringProperty()