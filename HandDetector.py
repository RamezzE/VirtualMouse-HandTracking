import mediapipe as mp
import cv2

class HandDetector:
    self.LEFT_HAND = 0
    self.RIGHT_HAND = 1

    # Constructor
    def __init__(self):
        pass

    # This function returns the image with the landmarks of the hand drawn on it
    def findHands(self, img, draw=True):
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    mpDraw = mp.solutions.drawing_utils
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
        return img

    # This function returns the landmarks of the hand in a list
    def getLandmarks(self, img, handNo = self.RIGHT_HAND, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
        return lmList