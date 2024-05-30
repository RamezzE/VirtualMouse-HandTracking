import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window
from views.homeView import HomeScreen

class VirtualMouse(App):
    def build(self):
        screen = HomeScreen()
        return screen.getRoot()

if __name__ == '__main__':
    Window.fullscreen = True
    Window.size = (Window.width / 3, Window.height / 1.5)
    Window.fullscreen = False
        
    Window.minimum_width = 300
    Window.minimum_height = 500
    
    VirtualMouse().run()