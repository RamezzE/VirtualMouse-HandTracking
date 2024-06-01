from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.HomeScreen import HomeScreen
from screens.CameraScreen import CameraScreen
from kivy.core.window import Window

class VirtualMouse(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomeScreen(name='home'))
        self.camera_screen = CameraScreen(name='camera')
        self.sm.add_widget(self.camera_screen)
        return self.sm

    def on_stop(self):
        if hasattr(self.camera_screen, 'on_stop'):
            self.camera_screen.on_stop()

if __name__ == '__main__':
    # Window.fullscreen = 'auto'
    Window.size = (Window.width / 3, Window.height / 1.5)
    Window.minimum_width = 300
    Window.minimum_height = 500
    VirtualMouse().run()
