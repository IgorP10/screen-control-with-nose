import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Inicialização do MediaPipe Face Mesh e Hands
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

# Contador para integração temporal
frames_close_to_nose = 0
# Número de frames consecutivos para considerar cutucando o nariz
frames_threshold = 10

is_video_paused = False

def calculate_distance_3d(point1, point2):
    """Calcula a distância euclidiana entre dois pontos no espaço 3D."""
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

def is_hand_close_to_nose(hand_landmarks, face_landmarks, threshold_ratio):
    """Verifica se a mão está próxima ao nariz."""
    # Landmarks laterais do rosto para referência do limiar
    face_landmark_left = face_landmarks.landmark[234]
    face_landmark_right = face_landmarks.landmark[454]
    face_width = calculate_distance_3d(face_landmark_left, face_landmark_right)
    
    # Landmark 4 para a ponta do nariz no MediaPipe Face Mesh
    nose_landmark = face_landmarks.landmark[4]

    # Landmark 8 para a ponta do dedo indicador no MediaPipe Hands
    finger_tip_landmark = hand_landmarks.landmark[8]

    # Cálculo da distância entre a ponta do dedo e a ponta do nariz
    distance = calculate_distance_3d(nose_landmark, finger_tip_landmark)

    # O limiar é uma fração da largura do rosto
    threshold = face_width * threshold_ratio
    return distance < threshold

# Inicialização da câmera
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh, mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Inverter a imagem horizontalmente para não ficar como espelho.
        image = cv2.flip(image, 1)

        # Converter a imagem de BGR para RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Processar as detecções
        results_face = face_mesh.process(image)
        results_hand = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Limiar baseado na proporção da largura do rosto
        threshold_ratio = 0.1

        # Verifica se a mão está próxima ao nariz
        if results_hand.multi_hand_landmarks and results_face.multi_face_landmarks:
            for hand_landmarks in results_hand.multi_hand_landmarks:
                for face_landmarks in results_face.multi_face_landmarks:
                    if is_hand_close_to_nose(hand_landmarks, face_landmarks, threshold_ratio):
                        frames_close_to_nose += 1
                        if frames_close_to_nose > frames_threshold and not is_video_paused:
                            pyautogui.press('space')  # Pausa o vídeo se estiver tocando
                            is_video_paused = True
                            print("Vídeo pausado")
                    else:
                        frames_close_to_nose = max(0, frames_close_to_nose - 1)  # Decremento para filtrar ruídos temporais
                        if frames_close_to_nose == 0 and is_video_paused:
                            pyautogui.press('space')  # Dá play no vídeo se estiver pausado
                            is_video_paused = False
                            print("Vídeo tocando")
        
        cv2.imshow('MediaPipe Face Mesh and Hands', image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
