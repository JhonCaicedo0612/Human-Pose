from ultralytics import YOLO
import cv2
import socket
import numpy as np


# Load a model
model = YOLO('runs/pose/train/weights/best.pt')  # Cargar el modelo

#video_path = 'prueba.mp4'
# model(video_path, conf=0.7, save=True) #guardar como video

video_path = 0 # Permite utilizar la camara
cap = cv2.VideoCapture(video_path)

# comunicacion
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while cap.isOpened():
    success, frame = cap.read()


    if success:
        s = socket.socket()

        datos = np.array([])

        # Predict with the model
        results = model(frame, conf=0.8, save=True)  # predecir sobre imagen

        # impirmir keypoints

        kp = results[0].keypoints.xy
        #print("los keypoints son:", kp[0])

        keypoint = kp[0].cpu().numpy()


        if keypoint.any():

            brazo1x, brazo1y = keypoint[10] #el que esta a la izquierda de la pantalla

            cadera1x, cadera1y = keypoint[12]

            brazo2x, brazo2y = keypoint[9]

            cadera2x, cadera2y = keypoint[11]

            # pierna a la izquierda de la pantalla "Pierna derecha"
            pierna1x, pierna1y = keypoint[16]

            # pierna a la derecha de la pantalla "Pierna izquierda"
            pierna2x, pierna2y = keypoint[15]

            # se calcula el obsoluto de la distancia
            distancia1 = np.abs(brazo1x-cadera1x)

            distancia2 = np.abs(brazo2x-cadera2x)

            distancia3 = np.abs(pierna1x - cadera1x)

            distancia4 = np.abs(pierna2x - cadera2x)

            if distancia1 < 80:
                distancia1 = 0

            if distancia2 < 80:
                distancia2 = 0
            if distancia3 < 50:
                distancia3 = 0
            if distancia4 < 50:
                distancia4 = 0

            datos = [distancia1, distancia2, distancia3, distancia4]

            print(datos)

            # codigo para mandar a unity

            sock.sendto(str.encode(str(datos)), serverAddressPort)

        else:
            print(" no se a detectado ")


        # visualiza el resultado en el frame
        annotated_frame = results[0].plot()

        #annotated_frame = cv2.resize(annotated_frame, (540, 960))
        annotated_frame = cv2.resize(annotated_frame, (460, 240))
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Romper el ciclo
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

