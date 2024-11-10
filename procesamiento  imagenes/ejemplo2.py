import cv2
import numpy as np

img = cv2.imread('cubo.jpg')
num_rows, num_cols = img.shape[:2]
translation_matrix = np.float32([ [1,0,70], [0,1,110] ])
img_translation = cv2.warpAffine(img, translation_matrix, (num_cols, num_rows))
cv2.imshow('Translation', img_translation)
cv2.waitKey()
