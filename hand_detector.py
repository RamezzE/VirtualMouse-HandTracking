import mediapipe as mp
import cv2
import pyautogui
import math

class Hand_Detector:
    screen_width, screen_height = pyautogui.size()
    
    THUMB = 4
    INDEX = 8
    MIDDLE = 12
    RING = 16
    PINKY = 20
    
    # Constructor
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.mpHandsDetector = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
                
    def findHands(self, img, drawConnections = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.img_height, self.img_width, _ = img.shape
        self.results = self.mpHandsDetector.process(imgRGB)
        self.hands = self.results.multi_hand_landmarks
        
        if drawConnections:
            if not self.hands:
                return img
            
            for hand in self.hands:
                self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
            
        return img
    
    
    def highlightFingers(self, img, fingers = [THUMB, INDEX, MIDDLE, RING, PINKY]):
        if not self.hands:
            return img
        
        for hand in self.hands:
            landmarks = hand.landmark
      
            for id, landmark in enumerate(landmarks):
                if id not in fingers:
                    continue
                
                x = int(landmark.x * self.img_width)
                y = int(landmark.y * self.img_height)
                cv2.circle(img = img, center = (x, y), radius = 10, color = (255, 0, 0), thickness = cv2.FILLED)
                
        return img
    
    def getFingerPosition(self, fingerId, hand = 0):
        landmarks = self.getLandmarks(hand)
        if landmarks and fingerId < len(landmarks):
            finger = landmarks[fingerId]
            finger_x = int(finger.x * self.img_width)
            finger_y = int(finger.y * self.img_height)
            
            screen_x = int(self.screen_width / self.img_width * finger_x)
            screen_y = int(self.screen_height / self.img_height * finger_y)
            return finger_x, finger_y, screen_x, screen_y 
        return None, None, None, None

    
    def getLandmarks(self, hand = 0):
        if self.hands and hand < len(self.hands):
            return self.hands[hand].landmark
        return None
    
    def getFingersUp(self, hand = 0):
        if not self.hands:
            return [0,0,0,0,0]
        
        handType = self.results.multi_handedness[hand].classification[0].label
        lmList = self.getLandmarks(hand)
        
        fingersUp = []
                
        # Thumb
        # if handType == "Right":
        if handType == "Left":
            if lmList[self.THUMB].x > lmList[self.THUMB - 1].x:
                fingersUp.append(1)
            else:
                fingersUp.append(0)
        else:
            if lmList[self.THUMB].x < lmList[self.THUMB - 1].x:
                fingersUp.append(1)
            else:
                fingersUp.append(0)

        # 4 Fingers
        for fingerId in [self.INDEX, self.MIDDLE, self.RING, self.PINKY]:
            # Check if the current finger is up
            if lmList[fingerId].y < lmList[fingerId - 2].y:
                fingersUp.append(1)  # Finger is up
            else:
                fingersUp.append(0)  # Finger is down
        
        return fingersUp
    
    def isFingerOnlyUp(self, finger, hand = 0):
        fingers = self.getFingersUp(hand)
        if not fingers:
            return False
        
        return sum (fingers) == 1 and fingers[int(finger / 4) -1] == 1
    
    def getDistance(self, f1, f2, img = None, color = (255, 0, 255), scale = 5, draw = True):
        x1, y1 = self.getFingerPosition(f1)[0:2]
        x2, y2 = self.getFingerPosition(f2)[0:2]
        
        if x1 is None or x2 is None or y1 is None or y2 is None:
            return None, img
        
        distance = math.hypot(x2 - x1, y2 - y1)
        
        if img is not None:
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            # cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return distance, img

    