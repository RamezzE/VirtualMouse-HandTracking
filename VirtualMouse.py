import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from screens.HomeScreen import HomeScreen

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.lang import Builder

class VirtualMouse(App):
    def build(self):
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(), name='home')
        
        return sm
        
if __name__ == '__main__':
    Window.fullscreen = True
    Window.size = (Window.width / 3, Window.height / 1.5)
    Window.fullscreen = False
        
    Window.minimum_width = 300
    Window.minimum_height = 500
    
    VirtualMouse().run()