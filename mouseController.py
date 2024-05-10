import pyautogui
import time
class MouseController:
    
    pyautogui.FAILSAFE = False
    
    def __init__(self, screenSize):
        self.screenWidth, self.screenHeight = screenSize
        self.mouse_held = False
        
    def moveMouse(self, x, y, sensitivity = 1):
        if not x or not y:
            return
        
        pyautogui.moveTo(x * sensitivity, y * sensitivity)
        
    def moveMouse(self, pos, sensitivity = 1):
        x, y = pos
        if not x or not y:
            return
        
        roundNum = 50
        pyautogui.moveTo(round((x * sensitivity) / roundNum) * roundNum, round((y * sensitivity) / roundNum) * roundNum) 
        
    def clickMouse(self, button = 'left'):
        pyautogui.click(button = button)
        
    def clickMouse(self, button='left'):
        pyautogui.click(button = button)
        
    def __pressMouse(self, button='left'):
        if not self.mouse_held:
            pyautogui.mouseDown(button = button)
            self.mouse_held = True
        
    def __releaseMouse(self, button = 'left'):
        if self.mouse_held:
            pyautogui.mouseUp(button = button)
            self.mouse_held = False
    
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
                
    def getScreenSize(self):
        return self.screenWidth, self.screenHeight