from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.HomeScreen import HomeScreen
from screens.CameraScreen import CameraScreen
from views.screens.SettingsScreen import SettingsScreen
from kivy.core.window import Window

from kivy.clock import Clock

from db import Database
class VirtualMouse(App):
    
    def build(self):
        self.db = Database('db/actions.db', 'db/schema.sql')

        self.height = Window.height
        self.width = Window.width
        
        Window.bind(on_resize=self.resize)
                
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        Clock.schedule_once(lambda dt: self.sm.add_widget(CameraScreen(name='camera')), 0)
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
