from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from screens.HomeScreen import HomeScreen
from screens.CameraScreen import CameraScreen
from screens.SettingsScreen import SettingsScreen

from kivy.core.window import Window

class VirtualMouse(App):
    
    def build(self):
        
        self.height = Window.height
        self.width = Window.width
        
        Window.bind(on_resize=self.resize)
                
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.camera_screen = CameraScreen(name='camera')
        self.sm.add_widget(self.camera_screen)
        return self.sm

    def on_stop(self):
        if hasattr(self.camera_screen, 'on_stop'):
            self.camera_screen.on_stop()
            
    def resize(self, instance, value, *args):
        self.height = Window.height
        self.width = Window.width

if __name__ == '__main__':
    Window.size = (Window.width / 3, Window.height / 1.5)
    Window.minimum_width = 330
    Window.minimum_height = 500
    VirtualMouse().run()
