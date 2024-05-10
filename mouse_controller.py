import pyautogui

class Mouse_Controller:
    
    pyautogui.FAILSAFE = False
    
    def __init__(self, screen_size, click_threshold = 30):
        self.screen_width, self.screen_height = screen_size
        self.click_threshold = click_threshold
        self.sensivity = 1
        
    def moveMouse(self, x, y, sensitivity = -1):
        if sensitivity == -1:
            sensitivity = self.sensivity
        if not x or not y:
            return
        
        pyautogui.moveTo(x * sensitivity, y * sensitivity)
        
    def moveMouse(self, pos, sensitivity = -1):
        x, y = pos
        if sensitivity == -1:
            sensitivity = self.sensivity
        if not x or not y:
            return
        
        pyautogui.moveTo(x * sensitivity, y * sensitivity)
        
    def getScreenSize(self):
        return self.screen_width, self.screen_height