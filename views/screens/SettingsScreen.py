from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window

from views.components.settings import ChooseSettingButton, DropdownRow, OnOffRow, SliderRow, GestureRow
from views.components.CustomDropdown import CustomDropdown

from presenters import SettingsPresenter

from kivy.lang import Builder

Builder.load_file('kv/SettingsComponents.kv')

class SettingsScreen(Screen):
    gesture_options = []

    selected_setting = StringProperty(None)

    row_height = NumericProperty()
    gesture_row_height = NumericProperty()
    
    Builder.load_file('kv/SettingsScreen.kv')

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.size = Window.size
        self.pos = Window._pos

        self.row_height = self.height * 0.11
        self.gesture_row_height = self.row_height * 1.5
        
        self.bind(size=self.resize)
        
        self.presenter = SettingsPresenter(self)
        
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size
    
    def switch_screen(self, screen_name, direction):
        self.manager.transition.direction = direction
        self.manager.current = screen_name
    
    def select_setting(self, button_id):
        self.selected_setting = button_id

    def draw_settings(self, dt = 0):        
        
        self.ids['settings_header'].add_widget(ChooseSettingButton(text='General', settings=self))
        self.ids['settings_header'].add_widget(ChooseSettingButton(text='Gestures', settings=self))
                                     
        camera_options, selected_camera = self.presenter.get_camera_options()             
        self.ids['camera_settings'].add_widget(DropdownRow(text='Capturing Camera', settings=self, options= camera_options, selected = selected_camera,alternate_background=True))
        
        self.ids['detection_settings'].add_widget(SliderRow(text='Detection Confidence', settings=self, value = self.presenter.get_detection_confidence() ,alternate_background=True))
        self.ids['detection_settings'].add_widget(SliderRow(text='Tracking Confidence', settings=self, value = self.presenter.get_tracking_confidence()))
        
        self.ids['detection_settings'].add_widget(DropdownRow(text='Detection Responsiveness', settings=self, options=self.presenter.get_detection_responsiveness_options(), selected = self.presenter.get_detection_responsiveness(), alternate_background=True))
                
        self.ids['mouse_settings'].add_widget(OnOffRow(text='Toggle Relative Mouse', settings=self, on = self.presenter.is_relative_mouse(), alternate_background=True))
        self.relative_mouse_toggle = self.ids['mouse_settings'].children[-1]
        self.ids['mouse_settings'].add_widget(SliderRow(text='Relative Mouse Sensitivity', settings=self, value = self.presenter.get_relative_mouse_sensitivity()))
        self.ids['mouse_settings'].add_widget(SliderRow(text='Scroll Sensitivity', settings=self, value = self.presenter.get_scroll_sensitivity(), alternate_background=True))

        self.sliders = []
        for child in self.ids['detection_settings'].children:
            if isinstance(child, SliderRow):
                self.sliders.append(child.ids['slider'])
                
        for child in self.ids['mouse_settings'].children:
            if isinstance(child, SliderRow):
                self.sliders.append(child.ids['slider'])
        
        mappings = self.presenter.get_mappings()
        
        for i in range(len(mappings)):
            gesture_row = GestureRow(settings=self, alternate_background=(i % 2 == 0), image_source = App.get_running_app().icons['gestures'][f'gesture{i+1}'])
            gesture_row.ids['dropdown'].selected = self.gesture_options[mappings[i]-1]
            
            self.ids['gestures_table'].add_widget(gesture_row)
        
        self.ids['layout'].size = self.size

    def set_gesture_options(self, options):
        self.gesture_options = options
        
    def get_gesture_dropdowns(self):
        dropdowns = self._get_dropdowns(self.ids['gestures_table'])
        if dropdowns:
            dropdowns.reverse()
        return dropdowns
    
    def get_detection_dropdowns(self):
        dropdowns = self._get_dropdowns(self.ids['detection_settings'])
        if dropdowns:
            dropdowns.reverse()
        return dropdowns

    def _get_dropdowns(self, widget):
        custom_dropdowns = [child for child in widget.children if isinstance(child, CustomDropdown)]
        for child in widget.children:
            custom_dropdowns.extend(self._get_dropdowns(child))
        return custom_dropdowns
    
    def get_detection_confidence_slider(self):
        return self.sliders[1]
    
    def get_tracking_confidence_slider(self):
        return self.sliders[0]
    
    def get_relative_mouse_sensitivity_slider(self):
        return self.sliders[3]
    
    def get_scroll_sensitivity_slider(self):
        return self.sliders[2]
    
    def toggle_relative_mouse(self):
        self.relative_mouse_toggle.toggle()
        self.presenter.toggle_relative_mouse()
        
    def is_relative_mouse(self):
        return self.relative_mouse_toggle.is_on()
    
    def set_saving_settings(self, saving):
        self.manager.get_screen('camera').ids['GCP'].set_saving_settings(saving)

    def update_gcp_settings(self, detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse, scroll_sensitivity):
        self.manager.get_screen('camera').ids['GCP'].update_settings(detection_confidence, tracking_confidence, detection_responsiveness, relative_mouse_sensitivity, mappings, relative_mouse, scroll_sensitivity)
        
    def on_stop(self):
        self.presenter.switch_to_camera_screen()