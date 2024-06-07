from kivy.uix.actionbar import BoxLayout
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.clock import Clock
import numpy as np
import yaml
import threading

from components.settings import ChooseSettingButton, DropdownRow, SliderRow, OnOffRow, GestureRow
from components import Camera, CustomDropDown, CustomButton

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
        self.gesture_options = (np.array(self.db.get('Actions', columns_to_select='name'))).reshape(-1)
        self.numeric_gesture_options = {v: k for k, v in enumerate(self.gesture_options)}
        
        self.mappings = np.array((self.db.get('Mappings', columns_to_select='action_id'))).reshape(-1)
        
        self.rowHeight = self.height * 0.08
        self.gestureRowHeight = self.rowHeight * 1.5
        
        self.select('general')
                
        self.bind(size=self.resize)
        
        self.draw_settings()
        
    def draw_settings(self):
        ## Draw the settings headers
        settings_header = self.ids['settings_header']
        
        settings_header.add_widget(ChooseSettingButton(text='General', settings=self))
        settings_header.add_widget(ChooseSettingButton(text='Gestures', settings=self))
                
        ## Camera settings
        
        camera_indices = Camera.get_available_cameras(5)
        
        if len(camera_indices) <= 0:
            camera_indices = ['No Camera Found']
            selected_camera = 'No Camera Found'
        else:
            camera_indices = [f'Camera {i+1}' for i in camera_indices]
            selected_camera = self.db.get('CameraSettings', columns_to_select= ['value'],name='Camera')[0]
            
            if selected_camera == 'No Camera Found':
                selected_camera = 'Camera 1'
                
            elif selected_camera not in camera_indices:
                selected_camera = 'Camera 1'
                
        show_fps = self.db.get('CameraSettings', columns_to_select=['value'], name = 'Show FPS')[0]
            
        camera_settings = self.ids['camera_settings']
        camera_settings.add_widget(DropdownRow(text='Capturing Camera', settings=self, options= camera_indices, selected = selected_camera,alternate_background=True))
        camera_settings.add_widget(OnOffRow(text='Show FPS', settings=self))

        self.detection_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name = 'Detection Confidence')[0])
        self.tracking_confidence = float(self.db.get('DetectionSettings', columns_to_select=['value'], name = 'Tracking Confidence')[0])
        
        detection_settings = self.ids['detection_settings']
        detection_settings.add_widget(SliderRow(text='Detection Confidence', settings=self, value = int(self.detection_confidence * 100),alternate_background=True))
        detection_settings.add_widget(SliderRow(text='Tracking Confidence', settings=self, value = int(self.tracking_confidence * 100)))
       
        self.sliders = []
        for child in detection_settings.children:
            self.sliders.append(child.ids['slider'])
       
        gestures_table = self.ids['gestures_table']
        
        print(len(self.mappings))
        for i in range(len(self.mappings)):
            gesture_row = GestureRow(settings=self, alternate_background=(i % 2 == 0), image_source = self.icons['gestures'][f'gesture{i+1}'])
            gesture_row.ids['dropdown'].selected = self.gesture_options[self.mappings[i]-1]
            
            gestures_table.add_widget(gesture_row)
        
        self.ids['layout'].size = self.size
                            
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
        
    def toCameraScreen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'camera'
        
        threading.Thread(target=self.update_settings).start()
        
    def update_settings(self):
        self.manager.get_screen('camera').ids['GCP'].saving_settings = True
        self.update_general_settings()
        self.update_gesture_mappings()
        self.manager.get_screen('camera').ids['GCP'].saving_settings = False

        Clock.schedule_once(self.update_dependencies_loaded, 0)

    def update_general_settings(self):
        print("Updating general settings")
        
        if int(self.sliders[1].value)/100 != self.detection_confidence:
            self.db.update('DetectionSettings', {'value': int(self.sliders[0].value)/100}, name='Detection Confidence')
            self.detection_confidence = int(self.sliders[1].value)/100    
    
        if int(self.sliders[0].value)/100 != self.tracking_confidence:
            self.db.update('DetectionSettings', {'value': int(self.sliders[1].value)/100}, name='Tracking Confidence')
            self.tracking_confidence = int(self.sliders[0].value)/100
        
        self.manager.get_screen('camera').ids['GCP'].detection_confidence = self.detection_confidence    
        self.manager.get_screen('camera').ids['GCP'].tracking_confidence = self.tracking_confidence    
        
        self.manager.get_screen('camera').ids['GCP'].update_settings()
        
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
        indices_to_change = self.get_new_gesture_mappings()
        
        for i, (gesture_id, action_id) in enumerate(indices_to_change):
            self.db.update('Mappings', {'action_id': action_id}, gesture_id=gesture_id)
                
    def update_dependencies_loaded(self, dt):
        self.manager.get_screen('camera').ids['GCP'].mappings = self.mappings
        self.manager.get_screen('camera').ids['GCP'].saving_settings = False
        
    def get_new_gesture_mappings(self):
        dropdowns = self.getDropDowns(self.ids['gestures_table'])
        dropdowns.reverse()
        new_mappings = []
        
        for dropdown in dropdowns:
            new_mappings.append(self.numeric_gesture_options[dropdown.selected])
                
        mappings_to_change = []
        
        for i in range(len(self.mappings)):
            if self.mappings[i]-1 != new_mappings[i]:
                print(f"Changed: {i} {self.mappings[i]-1} -> {new_mappings[i]}")
                mappings_to_change.append([i, new_mappings[i]+1])
                self.mappings[i] = new_mappings[i]+1
                
        return mappings_to_change
