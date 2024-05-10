import pyautogui
import time
class Mouse_Controller:
    
    pyautogui.FAILSAFE = False
    
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        self.mouse_held = False
        
    def moveMouse(self, x, y, sensitivity = 1):
        if not x or not y:
            return
        
        pyautogui.moveTo(x * sensitivity, y * sensitivity)
        
    def moveMouse(self, pos, sensitivity = 1):
        x, y = pos
        if not x or not y:
            return
        
        pyautogui.moveTo(x * sensitivity, y * sensitivity) 
        
    def clickMouse(self, button = 'left'):
        pyautogui.click(button = button)
        
    def clickMouse(self, button='left'):
        pyautogui.click(button=button)
        
    def __pressMouse(self, button='left'):
        if not self.mouse_held:
            pyautogui.mouseDown(button=button)
            self.mouse_held = True
        
    def __releaseMouse(self, button='left'):
        if self.mouse_held:
            pyautogui.mouseUp(button=button)
            self.mouse_held = False
    
    def handleMousePress(self, fist_closed):
        if fist_closed:
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
        return self.screen_width, self.screen_height