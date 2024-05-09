import mediapipe as mp
import cv2

class Hand_Detector:
    LEFT_HAND = 0
    RIGHT_HAND = 1

    # Constructor
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        
    def process(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width, _ = img.shape
        self.results = self.hands.process(imgRGB)

    def drawHands(self, img, fingerIdsToDraw = [], drawConnections = True):
        hands = self.results.multi_hand_landmarks
        if not hands:
            return img
        
        for hand in hands:
            if drawConnections:
                self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)
                
            landmarks = hand.landmark
                
            for id, landmark in enumerate(landmarks):
                if id in fingerIdsToDraw:
                    x = int(landmark.x * self.img_width)
                    y = int(landmark.y * self.img_height)
                    cv2.circle(img = img, center = (x, y), radius = 10, color = (255, 0, 0), thickness = cv2.FILLED)
                            
        return img