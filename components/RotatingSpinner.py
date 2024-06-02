from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.graphics import Color, Line, PushMatrix, PopMatrix, Rotate
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ColorProperty, NumericProperty

class RotatingSpinner(Widget):
    
    color = ColorProperty([0.1, 0.7, 0.8, 1])  
    numLines = NumericProperty(12)            
    lineThickness = NumericProperty(2)        
    animationDuration = NumericProperty(5)   
    gap = NumericProperty(15)
    
    size_hint = 1, 1      
    pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    
    def __init__(self, **kwargs):
        super(RotatingSpinner, self).__init__(**kwargs)

        with self.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.origin = self.center
            self.rot.angle = 0
            self.rot.axis = (0, 0, 1)

        with self.canvas:
            Color(*self.color)
            num_lines = 12
            angle_step = 360 / num_lines
            line_thickness = 2
            gap = 5  # degrees gap for each segment
            circle_radius = min(self.size) / 2
            for i in range(num_lines):
                Line(circle=(self.center_x, self.center_y, circle_radius, i * angle_step, i * angle_step + angle_step - gap),
                     width=line_thickness)

        with self.canvas.after:
            PopMatrix()

        self.anim = Animation(angle=360, duration=self.animationDuration)
        self.anim += Animation(angle=0, duration=0)
        self.anim.repeat = True
        self.anim.start(self.rot)

        self.bind(size=self.update_graphics_pos, pos=self.update_graphics_pos)

    def update_graphics_pos(self, *args):
        self.rot.origin = self.center
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            angle_step = 360 / self.numLines
            self.radius = min(self.size) / 2
            
            for i in range(self.numLines):
                Line(circle=(self.center_x, self.center_y, self.radius, i * angle_step, i * angle_step + angle_step - self.gap),
                     width=self.lineThickness)

class MyApp(App):
    def build(self):
        root = FloatLayout()
        spinner = RotatingSpinner(
            size_hint = (0.2, 0.2),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5},
            numLines = 3,
            lineThickness = 2,
            animationDuration = 3,
            gap = 50,
            color = [1, 1, 1, 0.87]
        )
        root.add_widget(spinner)
        return root

if __name__ == '__main__':
    MyApp().run()
