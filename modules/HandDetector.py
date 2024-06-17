import mediapipe as mp
import cv2
import math
import warnings
warnings.filterwarnings("ignore")
class HandDetector:
    WRIST = 0
    THUMB = 4
    INDEX = 8
    MIDDLE = 12
    RING = 16
    PINKY = 20
    
    def __init__(self, detection_con = 0.5, track_con = 0.5):
        
        self.mp_hands = mp.solutions.hands
        self.mp_hands_detector = self.mp_hands.Hands(min_detection_confidence = detection_con, min_tracking_confidence = track_con, max_num_hands = 1)
        self.mp_draw = mp.solutions.drawing_utils
        
    def set_confidence(self, detection_con = 0.5, track_con = 0.5):
        self.mp_hands_detector = self.mp_hands.Hands(min_detection_confidence = detection_con, min_tracking_confidence = track_con, max_num_hands = 1)
        
    def find_hands(self, img, draw_connections = True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        self.imgHeight, self.imgWidth, _ = img.shape
        self.results = self.mp_hands_detector.process(img_rgb)
        self.hands = self.results.multi_hand_landmarks
        self.hand_label = self.results.multi_handedness[0].classification[0].label if self.results.multi_handedness else 'No Hand Detected'
        
        if draw_connections:
            if not self.hands:
                return img
            
            for hand in self.hands:
                self.mp_draw.draw_landmarks(img, hand, self.mp_hands.HAND_CONNECTIONS)
            
        return img
    
    def highlight_fingers(self, img, fingers = [THUMB, INDEX, MIDDLE, RING, PINKY]):
        if not self.hands:
            return img
        
        for hand in self.hands:
            landmarks = hand.landmark
      
            for id, landmark in enumerate(landmarks):
                if id not in fingers:
                    continue
                
                x = int(landmark.x * self.imgWidth)
                y = int(landmark.y * self.imgHeight)
                cv2.circle(img = img, center = (x, y), radius = 10, color = (255, 0, 0), thickness = cv2.FILLED)
                
        return img
    
    def get_finger_position(self, fingerId, hand = 0):
        landmarks = self.get_landmarks(hand)
        if landmarks and fingerId < len(landmarks):
            finger = landmarks[fingerId]
            x = int(finger.x * self.imgWidth)
            y = int(finger.y * self.imgHeight)
            
            return x, y
        return None, None
    
    def get_finger_z(self, fingerId, hand = 0):
        landmarks = self.get_landmarks(hand)
        if landmarks and fingerId < len(landmarks):
            return landmarks[fingerId].z
        return None

    
    def get_landmarks(self, hand = 0):
        try:
            if self.hands and hand < len(self.hands):
                return self.hands[hand].landmark
            return None
        except:
            return None
    
    def get_fingers_up(self, hand = 0):
        if not self.hands:
            return None
        
        hand_type = self.results.multi_handedness[hand].classification[0].label
        lm_list = self.get_landmarks(hand)
        
        fingers_up = []
                
        if hand_type == "Left":
            if lm_list[self.THUMB].x > lm_list[self.THUMB - 1].x:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        else:
            if lm_list[self.THUMB].x < lm_list[self.THUMB - 1].x:
                fingers_up.append(1)
            else:
                fingers_up.append(0)

        for fingerId in [self.INDEX, self.MIDDLE, self.RING, self.PINKY]:
            if lm_list[fingerId].y < lm_list[fingerId - 2].y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        return fingers_up
    
    def is_finger_only_up(self, finger, hand = 0):
        fingers = self.get_fingers_up(hand)
        if not fingers:
            return False
        
        return sum (fingers) == 1 and fingers[int(finger / 4) -1] == 1
    
    def is_fist_closed(self, hand = 0):
        fingers = self.get_fingers_up(hand)
        if not fingers:
            return None
        
        return sum(fingers) == 0
    
    def get_distance(self, f1, f2, img = None, color = (255, 0, 255), scale = 5, draw = True):
        x1, y1 = self.get_finger_position(f1)
        x2, y2 = self.get_finger_position(f2)
        
        if x1 is None or x2 is None or y1 is None or y2 is None:
            return None, img
        
        distance = math.hypot(x2 - x1, y2 - y1)
        
        if img is not None:
            cv2.circle(img, (x1, y1), scale, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), scale, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, max(1, scale // 3))
            # cv2.circle(img, (cx, cy), scale, color, cv2.FILLED)

        return distance, img

    def is_distance_within(self, f1, f2, distance = 25):
        dist, _ = self.get_distance(f1, f2)
        return dist is not None and dist < distance
    
    def get_hand_orientation(self, hand=0):
        return self.hand_label