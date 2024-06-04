import numpy as np
import mouse
import time

class MouseController:
    
    LOW_SENSITIVITY = 1
    NORMAL_SENSITIVITY = 2
    
    def __init__(self, screenSize):
        self.screenWidth, self.screenHeight = screenSize
        self.mouseHeld = False
        self.justClickedLeft = self.justClickedRight = False
        self.prevPos, self.prevPosTime = None, None
        self.handSpeed = 0
        self.relativeMouse = False
        self.rangeX, self.rangeY = None, None
        
    def toggleRelativeMouse(self):
        self.relativeMouse = not self.relativeMouse
        
    def moveMouse(self, pos, imgShape):
        if not pos:
            return
        
        if self.prevPos is None:
            self.prevPos = pos
            return
        
        if self.rangeX is None or self.rangeY is None:
            self.rangeX = [imgShape[0]*0.2, imgShape[0]*1.1]   
            self.rangeY = [imgShape[1]*0.05, imgShape[1]*0.5]
        
        if self.relativeMouse:
            self.__moveMouseRelative(pos)
            return
        else:
            self.__moveMouseAbsolute(pos)
        
    def __moveMouseAbsolute(self, pos):
        
        x = np.interp(pos[0], (self.rangeX[0], self.rangeX[1]), (0, self.screenWidth))
        y = np.interp(pos[1], (self.rangeY[0], self.rangeY[1]), (0, self.screenHeight))
            
        mouse.move(x, y)
        
    def __moveMouseRelative(self, pos, sensitivityScale = 0.75):
        
        x = np.interp(pos[0], (self.rangeX[0], self.rangeX[1]), (0, self.screenWidth))
        y = np.interp(pos[1], (self.rangeY[0], self.rangeY[1]), (0, self.screenHeight))
        
        prevX = np.interp(self.prevPos[0], (self.rangeX[0], self.rangeX[1]), (0, self.screenWidth))
        prevY = np.interp(self.prevPos[1], (self.rangeY[0], self.rangeY[1]), (0, self.screenHeight))
        
        self.prevPos = pos
        
        newX = (x - prevX) * sensitivityScale
        newY = (y - prevY) * sensitivityScale
                
        mouse.move(newX, newY, absolute = False)
        
    def resetMousePos(self):
        self.prevPos = None
        
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
            
    def __calculateSpeed(self, pos):
        
        prevX, prevY = self.prevPos
        x, y = pos
        
        currentTime = time.time()
        
        if self.prevPosTime is None:
            self.prevPosTime = currentTime
            return 0
        
        elapsedTime = currentTime - self.prevPosTime
                  
        distanceX = abs(x - prevX)
        distanceY = abs(y - prevY)
        
        distance = np.sqrt(distanceX ** 2 + distanceY ** 2) 
        
        if elapsedTime <= 0:
            return 0
        
        self.prevPosTime = currentTime
        self.prevPos = pos
                
        self.handSpeed = distance[0] / elapsedTime
        
        return self.handSpeed
    
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