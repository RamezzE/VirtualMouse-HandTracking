from kivy.config import Config

Config.set('graphics', 'maxfps', '60')
Config.set('graphics', 'width', '0')
Config.set('graphics', 'height', '0')

from kivy.core.window import Window
Window.hide()

import os 
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import yaml

with open('paths.yaml', 'r') as f:
    paths = yaml.safe_load(f)
    
icons = paths['assets']['icons']
fonts = paths['assets']['fonts']

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from KivyOnTop import register_topmost

from views.screens import SettingsScreen, CameraFeedbackScreen, HomeScreen

from kivy.clock import Clock

from db.db import Database

db = Database(paths['db']['actions'], paths['db']['schema'])

class VirtualMouse(App):
    title = 'Virtual Mouse'
    
    def build(self):
        self.paths = paths
        self.fonts = fonts
        self.icons = icons
        self.db = db
        
        register_topmost(Window, self.title)
        
                
        Window.bind(on_resize=self.resize)
                
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        
        self._show_window()
        
        Clock.schedule_once(lambda dt: self.sm.add_widget(CameraFeedbackScreen(name='camera')), 0)
        self.sm.add_widget(SettingsScreen(name='settings'))
        return self.sm
    
    def _show_window(self):
        Window.size = (360, 500)
        Window.minimum_width = 360
        Window.minimum_height = 500
        self.height = Window.height
        self.width = Window.width
        self.icon = icons['app']
        Window.show()

    def on_stop(self):
        Window.hide()
        for screen in self.sm.screens:
            if hasattr(screen, 'on_stop'):
                screen.on_stop()
            
    def resize(self, instance, value, *args):
        self.height = Window.height
        self.width = Window.width

if __name__ == '__main__':
    VirtualMouse().run()
