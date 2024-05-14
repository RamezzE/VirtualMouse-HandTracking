import time
import numpy as np
import mouse

class MouseController:
    def __init__(self, screenSize):
        self.screenWidth, self.screenHeight = screenSize
        self.mouseHeld = False
        self.justClickedLeft = self.justClickedRight = False
        
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
        justClicked = False
        if button == 'left':
            justClicked = self.justClickedLeft
            
        elif button == 'right':
            justClicked = self.justClickedRight
            
        else: return
        
        if justClicked:
            return
        
        mouse.click(button)
        
        if button == 'left':
            self.justClickedLeft = True
        else: self.justClickedRight = True 
        
    def doubleClick(self, button = 'left'):
        if button == 'left':
            if not self.justClickedLeft:
                mouse.double_click(button)
                self.justClickedLeft = True
                
        elif button == 'right':
            if not self.justClickedRight:
                mouse.double_click(button)
                self.justClickedRight = True
        
    def __pressMouse(self, button = 'left'):
        if not self.mouseHeld:
            # print('Mouse Held')
            mouse.press(button)
            self.mouseHeld = True
        
    def __releaseMouse(self, button = 'left'):
        if self.mouseHeld:
            # print('Mouse Released')
            mouse.release(button)
            self.mouseHeld = False
    
    def handleMousePress(self, condition, button = 'left'):
        if condition:
            self.__pressMouse(button)
            return True
        else:
            self.__releaseMouse(button)
            return False            
        
    def resetClick(self, button = 'both'):
        if button == 'left':
            self.justClickedLeft = False
        elif button == 'right': self.justClickedRight = False
        else:
            self.justClickedLeft = self.justClickedRight = False
            
    def handleScroll(self, condition = True):
        if condition:
            mouse.wheel(1)
        else: mouse.wheel(-1)