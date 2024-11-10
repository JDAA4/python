import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()

fram_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('salida.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (fram_width, frame_height))

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede recibir el cuadro. Saliendo...")
        break
    out.write(frame)
    cv2.imshow('cuadro', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()