import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Carregar imagem
image = cv2.imread('images/image.png')  # Substitua pelo caminho correto da imagem
results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

# Desenhar landmarks no rosto
if results.multi_face_landmarks:
    for face_landmarks in results.multi_face_landmarks:
        for idx, landmark in enumerate(face_landmarks.landmark):
            x = int(landmark.x * image.shape[1])
            y = int(landmark.y * image.shape[0])
            cv2.circle(image, (x, y), 1, (0, 255, 0), -1)
            cv2.putText(image, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)

cv2.imshow('MediaPipe FaceMesh with Landmark Numbers', image)
cv2.imwrite('images/image_result.png', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
