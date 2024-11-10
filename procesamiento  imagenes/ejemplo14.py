import cv2
import numpy as np
img1 =np.zeros((400,600),dtype=np.uint8)
img1[100:300,200:400]=168
cv2.imshow('Imagen1',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()