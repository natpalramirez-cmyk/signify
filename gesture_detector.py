import cv2
import mediapipe as mp
import time
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GestureDetector:
    def __init__(self):
        try:
            self.mp_hands = mp.solutions.hands
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=Config.MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=Config.MIN_TRACKING_CONFIDENCE
            )
            self.mp_drawing = mp.solutions.drawing_utils
            self.current_letter = ""
            self.word = ""
            self.last_time = time.time()
            logger.info("Gesture detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize gesture detector: {e}")
            raise

    def count_fingers(self, hand_landmarks):
        """Count the number of extended fingers"""
        try:
            fingers = []
            
            # Thumb
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Other four fingers
            finger_tips = [8, 12, 16, 20]
            finger_pips = [6, 10, 14, 18]
            
            for tip, pip in zip(finger_tips, finger_pips):
                if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                    fingers.append(1)
                else:
                    fingers.append(0)
            
            return sum(fingers)
        except Exception as e:
            logger.error(f"Error counting fingers: {e}")
            return 0

    def detect_gesture(self, frame):
        """Detect hand gestures in the frame"""
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb_frame)
            
            detected_letter = ""
            
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
                    
                    # Count fingers and map to letter
                    finger_count = self.count_fingers(hand_landmarks)
                    detected_letter = Config.GESTURE_MAP.get(finger_count, "")
                    
                    # Update current letter if different
                    if detected_letter and detected_letter != self.current_letter:
                        self.current_letter = detected_letter
                        self.last_time = time.time()
            
            # Add letter to word if held for required time
            current_time = time.time()
            if (self.current_letter and 
                current_time - self.last_time > Config.GESTURE_HOLD_TIME):
                self.word += self.current_letter
                self.last_time = current_time
                logger.info(f"Added letter '{self.current_letter}' to word. Current word: '{self.word}'")
            
            # Draw text on frame
            cv2.putText(frame, f"Letra: {self.current_letter}", (30, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(frame, f"Palabra: {self.word}", (30, 150),
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
            
            return frame, detected_letter, self.word
            
        except Exception as e:
            logger.error(f"Error detecting gesture: {e}")
            return frame, "", self.word

    def process_image(self, image_path):
        """Process a static image for gesture detection"""
        try:
            frame = cv2.imread(image_path)
            if frame is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            frame, detected_letter, word = self.detect_gesture(frame)
            return detected_letter, word
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            return "", ""

    def reset_word(self):
        """Reset the current word"""
        self.word = ""
        self.current_letter = ""
        logger.info("Word reset")

    def __del__(self):
        """Cleanup resources"""
        try:
            if hasattr(self, 'hands'):
                self.hands.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
