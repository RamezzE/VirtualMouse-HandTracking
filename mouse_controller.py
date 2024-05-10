import pyautogui

class Mouse_Controller:
    
    pyautogui.FAILSAFE = False
    
    def __init__(self, screen_size):
        self.screen_width, self.screen_height = screen_size
        
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
        
        
    def getScreenSize(self):
        return self.screen_width, self.screen_height