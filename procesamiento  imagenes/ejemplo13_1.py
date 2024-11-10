import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
face_mask = cv2.imread("mascara.png").astype(np.uint8)
h_mask, w_mask = face_mask.shape[:2]

if face_cascade.empty():
    raise IOError('Error al cargar el archivo xml')

cap = cv2.VideoCapture(0)
scaling_factor = 0.5

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            h, w = int(1.4 * h), int(1.0 * w)
            y = int(y - 0.1 * h)
            roi = frame[y:y + h, x:x + w]
            face_mask_small = cv2.resize(face_mask, (w, h), interpolation=cv2.INTER_AREA)
            gray_mask = cv2.cvtColor(face_mask_small, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray_mask, 180, 255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)

            # Asegurarse de que ambos tengan el mismo tipo y forma
            roi = roi.astype(np.uint8)
            mask_inv = mask_inv.astype(np.uint8)

            # Ajustar el tamaño de la máscara a la región de interés (ROI)
            mask_inv_resized = cv2.resize(mask_inv, (w, h))

            # Aplicar la máscara
            masked_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            masked_roi = cv2.bitwise_and(masked_roi, masked_roi, mask=mask_inv_resized)

            masked_face = cv2.bitwise_and(face_mask_small, face_mask_small, mask=mask)
            masked_roi = cv2.bitwise_and(roi, roi, mask=mask_inv_resized)
            frame[y:y + h, x:x + w] = cv2.add(masked_face, masked_roi)

    cv2.imshow('Face Detector', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()




