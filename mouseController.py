import time
import numpy as np
import mouse
class MouseController:
    def __init__(self, screenSize):
        self.screenWidth, self.screenHeight = screenSize
        self.mouseHeld = False
        self.prevPos = None
        
    def moveMouse(self, pos, imgShape):
        x, y = pos
        if not x or not y:
            return
                
        rangeX = [imgShape[0]*0.2, imgShape[0]*1.1]   
        rangeY = [imgShape[1]*0.1, imgShape[1]*0.5]
                
        x = np.interp(x, (rangeX[0], rangeX[1]), (0, self.screenWidth))
        y = np.interp(y, (rangeY[0], rangeY[1]), (0, self.screenHeight))
                
        prevX, prevY = mouse.get_position()   
        
        if (abs(x - prevX) > 15 or abs(y - prevY) > 15):
            mouse.move(x, y) 
    
        
    def clickMouse(self, button = 'left'):
        mouse.click(button)
        
    def __pressMouse(self, button = 'left'):
        if not self.mouseHeld:
            mouse.press(button)
            self.mouseHeld = True
        
    def __releaseMouse(self, button = 'left'):
        if self.mouseHeld:
            mouse.release(button)
            self.mouseHeld = False
    
    def handleMousePress(self, fistClosed):
        if fistClosed:
            self.__pressMouse()
            return True
        else:
            self.__releaseMouse()
            return False        
    def handleMousePressThread(self, func):
        while True:
            if self.handleMousePress(func()):
                time.sleep(0.1)