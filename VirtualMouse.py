from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from views.screens import SettingsScreen, CameraFeedbackScreen, HomeScreen
from kivy.core.window import Window

from kivy.clock import Clock

from db.db import Database

import yaml
class VirtualMouse(App):
    
    def build(self):
        
        with open('paths.yaml', 'r') as f:
            self.paths = yaml.safe_load(f)
            
        self.fonts = self.paths['assets']['fonts']
        self.icons = self.paths['assets']['icons']
        
        self.db = Database(self.paths['db']['actions'], self.paths['db']['schema'])

        self.height = Window.height
        self.width = Window.width
        
        Window.bind(on_resize=self.resize)
                
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        Clock.schedule_once(lambda dt: self.sm.add_widget(CameraFeedbackScreen(name='camera')), 0)
        self.sm.add_widget(SettingsScreen(name='settings'))
        return self.sm

    def on_stop(self):
        for screen in self.sm.screens:
            if hasattr(screen, 'on_stop'):
                screen.on_stop()
            
    def resize(self, instance, value, *args):
        self.height = Window.height
        self.width = Window.width

if __name__ == '__main__':
    Window.size = (350, 500)
    Window.minimum_width = 350
    Window.minimum_height = 500
    VirtualMouse().run()
