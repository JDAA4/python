import cv2
import numpy as np

img = cv2.imread('flor.png')
texto = 'Flor'
puntoA = (170, 80)
puntoB = (320, 80)
puntoC= (320 ,260)
puntoD = (170, 260)
centro = (166, 259)
radio = 50
img = cv2.circle(img, centro, radio, (0, 255, 0), thickness=3, lineType=cv2.LINE_AA)
#img = cv2.line(img, puntoA, puntoB, (255, 0, 00), thickness=3, lineType=cv2.LINE_AA)
#img = cv2.line(img, puntoB, puntoC, (255, 0, 00), thickness=3, lineType=cv2.LINE_AA)
#img = cv2.line(img, puntoC, puntoD, (255, 0, 00), thickness=3, lineType=cv2.LINE_AA)
#img = cv2.line(img, puntoD, puntoA, (255, 0, 00), thickness=3, lineType=cv2.LINE_AA)   
img = cv2.rectangle(img, puntoA, puntoC, (255, 0, ), thickness=3, lineType=cv2.LINE_AA)
cv2.imshow('imagen', img)
print(img.shape)
#img_crop = img[145:260, 190:315]
#cv2.imshow('imagen recortada', img_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
