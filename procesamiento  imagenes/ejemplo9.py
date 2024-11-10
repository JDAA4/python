import cv2

img = cv2.imread('test.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_2= cv2.GaussianBlur(img, (3, 3), 0)
sobel_x = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
sobel_y = cv2.Sobel(src=img, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
sobel_xy = cv2.Sobel(src=img_2, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
bordes = cv2.Canny(image=img_2, threshold1=100, threshold2=200)

cv2.imshow('Bordes en eje X y Y', bordes)
cv2.waitKey(0)