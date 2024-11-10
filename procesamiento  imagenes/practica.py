import cv2
import numpy as np

def cartoonize_image(img, ds_factor, sketch_mode):
    # Convertimos la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Aplicamos un suavizado a la imagen
    gray = cv2.medianBlur(gray, 7)
    # Detectamos los bordes en la imagen y los invertimos
    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    if sketch_mode:
        return cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    img_small = cv2.resize(img, None, fx=1.0/ds_factor, fy=1.0/ds_factor, interpolation=cv2.INTER_AREA)
    num_repetitions = 10
    sigma_color = 5
    sigma_space = 7
    size = 5
    for i in range(num_repetitions):
        img_small = cv2.bilateralFilter(img_small, size, sigma_color, sigma_space)
    img_output = cv2.resize(img_small, None, fx=ds_factor, fy=ds_factor, interpolation=cv2.INTER_LINEAR)
    dst = np.zeros(gray.shape)
    dst = cv2.bitwise_and(img_output, img_output, mask=mask)
    return dst

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
    frame = cartoonize_image(frame, 4, False)
    out.write(frame)
    
    cv2.imshow('cuadro', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
#out.release()
cv2.destroyAllWindows()