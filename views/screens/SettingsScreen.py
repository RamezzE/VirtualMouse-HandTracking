from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.core.window import Window

from views.components.settings import ChooseSettingButton, DropdownRow, OnOffRow, SliderRow, GestureRow
from views.components import CustomDropdown

from presenters.SettingsPresenter import SettingsPresenter

from kivy.lang import Builder

Builder.load_file('views/components/settings/SettingsComponents.kv')


class SettingsScreen(Screen):
    gesture_options = []

    selected = StringProperty(None)

    rowHeight = NumericProperty()
    gestureRowHeight = NumericProperty()

    thread_loaded = BooleanProperty(False)
    saving_settings = BooleanProperty(False)
    show_loading = BooleanProperty(True)
    status = StringProperty()
    current_fps = StringProperty()
    detection_confidence = NumericProperty()
    tracking_confidence = NumericProperty()
    
    Builder.load_file('views/screens/SettingsScreen.kv')

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.size = Window.size
        self.pos = Window._pos
        
        SettingsPresenter(self)

        self.rowHeight = self.height * 0.08
        self.gestureRowHeight = self.rowHeight * 1.5
        
        self.select('general')
        self.bind(size=self.resize)
        
    def set_presenter(self, presenter):
        self.presenter = presenter
        
    def set_fonts(self, fonts):
        self.fonts = fonts

    def set_icons(self, icons):
        self.icons = icons

    def set_gesture_options(self, options):
        self.gesture_options = options

    def set_mappings(self, mappings):
        self.mappings = mappings

    def set_detection_confidence(self, value):
        self.detection_confidence = value

    def set_tracking_confidence(self, value):
        self.tracking_confidence = value

    def set_camera_options(self, options):
        self.camera_options = options

    def set_selected_camera(self, camera):
        self.selected_camera = camera

    def set_show_fps(self, show_fps):
        self.show_fps = show_fps

    def draw_settings(self):
        settings_header = self.ids['settings_header']
        
        settings_header.add_widget(ChooseSettingButton(text='General', settings=self))
        settings_header.add_widget(ChooseSettingButton(text='Gestures', settings=self))
                                                    
        self.ids['camera_settings'].add_widget(DropdownRow(text='Capturing Camera', settings=self, options= self.camera_options, selected = self.selected_camera,alternate_background=True))
        self.ids['camera_settings'].add_widget(OnOffRow(text='Show FPS', settings=self))
        
        self.ids['detection_settings'].add_widget(SliderRow(text='Detection Confidence', settings=self, value = int(self.detection_confidence * 100),alternate_background=True))
        self.ids['detection_settings'].add_widget(SliderRow(text='Tracking Confidence', settings=self, value = int(self.tracking_confidence * 100)))

        self.sliders = []
        for child in self.ids['detection_settings'].children:
            self.sliders.append(child.ids['slider'])

        gestures_table = self.ids['gestures_table']
        
        for i in range(len(self.mappings)):
            gesture_row = GestureRow(settings=self, alternate_background=(i % 2 == 0), image_source = self.icons['gestures'][f'gesture{i+1}'])
            gesture_row.ids['dropdown'].selected = self.gesture_options[self.mappings[i]-1]
            
            gestures_table.add_widget(gesture_row)
        
        self.ids['layout'].size = self.size
    
    def resize(self, instance, value):
        self.size = instance.size
        self.pos = Window._pos
        self.ids['layout'].size = self.size

    def select(self, button_id):
        self.selected = button_id

    def to_camera_screen(self):
        self.presenter.to_camera_screen()

    def switch_to_camera_screen(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'camera'

    