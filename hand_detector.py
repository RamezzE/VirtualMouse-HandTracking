import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui

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
        
        self.detector = HandDetector(detectionCon = 0.8)
        
    def findHands(self, img, drawConnections = True, drawAll = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width, _ = img.shape
        self.results = self.mpHandsDetector.process(imgRGB)
        self.hands = self.results.multi_hand_landmarks
        
        self.CV_hands, img = self.detector.findHands(img, drawAll)
        
        if drawAll:
            return img
        
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
            x = int(finger.x * self.img_width)
            y = int(finger.y * self.img_height)
            
            x = int(self.screen_width / self.img_width * x)
            y = int(self.screen_height / self.img_height * y)
            return x, y 
        return None, None

    
    def getLandmarks(self, hand = 0):
        if self.hands and hand < len(self.hands):
            return self.hands[hand].landmark
        return None
    
    def getFingersUp(self, hand = 0):
        if not self.CV_hands or hand >= len(self.CV_hands):
            return [0, 0, 0, 0, 0]
        
        return self.detector.fingersUp(self.CV_hands[hand])
    
    def isFingerOnlyUp(self, finger, hand = 0):
        fingers = self.getFingersUp(hand)
        if not fingers:
            return False
        
        return sum (fingers) == 1 and fingers[int(finger / 4) -1] == 1
    