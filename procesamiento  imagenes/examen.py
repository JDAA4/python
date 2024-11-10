import cv2

cap =cv2.VideoCapture(0)
grey = False
yuv = False
hsv = False
normal = True
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        video = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        if normal:
            cv2.imshow('camara', video)
            
        elif grey:
            video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('camara', video)
            
        elif yuv:
            video = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
            cv2.imshow('camara', video)
            
        elif hsv:
            video = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.imshow('camara', video)
            
        key = cv2.waitKey(1) & 0xFF
        cv2.imshow('camara', video)
        if  key in [ord('q'), ord('x')]:
            break
        elif key == ord('g'):
            grey = True
            normal = False
            yuv = False
            hsv = False
        elif key == ord('y'):
            yuv = True
            normal = False
            grey = False
            hsv = False
        elif key == ord('h'):
            hsv = True
            normal = False
            grey = False
            yuv = False
        elif key == ord('n'):
            normal = True
            grey = False
            yuv = False
            hsv = False
    else:
        break
cap.release()
cv2.destroyAllWindows()