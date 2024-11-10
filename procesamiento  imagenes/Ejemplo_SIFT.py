import cv2 
 
img = cv2.imread('mariposa.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
sift = cv2.SIFT_create()
kp = sift.detect(gray,None)
 
img=cv2.drawKeypoints(gray,kp,img)
 
cv2.imshow('sift_keypoints',img)
cv2.waitKey()
cv2.imwrite('mariposa_SIFT.jpg',img)