import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import logging

# Configuration settings
FRAMES_THRESHOLD = 10
THRESHOLD_RATIO = 0.1

# Initialize logging
logging.basicConfig(level=logging.INFO)

def init_mediapipe():
    """Initializes and returns necessary MediaPipe solutions."""
    face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    hands = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    return face_mesh, hands

def calculate_distance_3d(point1, point2):
    """Calculates the Euclidean distance between two 3D points."""
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

def is_hand_close_to_nose(hand_landmarks, face_landmarks, face_width):
    """Checks if the hand is close to the nose based on landmark proximity."""
    nose_landmark = face_landmarks.landmark[4]  # Landmark for the tip of the nose
    finger_tip_landmark = hand_landmarks.landmark[8]  # Landmark for the tip of the index finger
    
    distance = calculate_distance_3d(nose_landmark, finger_tip_landmark)
    threshold = face_width * THRESHOLD_RATIO
    return distance < threshold

def process_image(image, face_mesh, hands, frames_close_to_nose, is_video_paused):
    """Processes the image and updates counters and states as needed."""
    image = cv2.flip(image, 1)  # Mirror the image
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results_face = face_mesh.process(image_rgb)
    results_hand = hands.process(image_rgb)

    if results_hand.multi_hand_landmarks and results_face.multi_face_landmarks:
        for hand_landmarks in results_hand.multi_hand_landmarks:
            for face_landmarks in results_face.multi_face_landmarks:
                face_landmark_left = face_landmarks.landmark[234]
                face_landmark_right = face_landmarks.landmark[454]
                face_width = calculate_distance_3d(face_landmark_left, face_landmark_right)
                
                if is_hand_close_to_nose(hand_landmarks, face_landmarks, face_width):
                    frames_close_to_nose += 1
                    if frames_close_to_nose > FRAMES_THRESHOLD and not is_video_paused:
                        pyautogui.press('space')
                        is_video_paused = True
                        logging.info("Video paused")
                else:
                    if frames_close_to_nose > 0:
                        frames_close_to_nose -= 1
                    if frames_close_to_nose == 0 and is_video_paused:
                        pyautogui.press('space')
                        is_video_paused = False
                        logging.info("Video playing")
    
    return image, frames_close_to_nose, is_video_paused

def main():
    logging.info("Starting application...")
    frames_close_to_nose = 0
    is_video_paused = False
    face_mesh, hands = init_mediapipe()
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Failed to open camera.")
        return

    try:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                logging.info("Ignoring empty camera frame.")
                continue

            image, frames_close_to_nose, is_video_paused = process_image(image, face_mesh, hands, frames_close_to_nose, is_video_paused)
            cv2.imshow('MediaPipe Face Mesh and Hands', image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
