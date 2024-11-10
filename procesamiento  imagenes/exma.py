import cv2

cap =cv2.VideoCapture(0)
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        video = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
        key = cv2.waitKey(1) & 0xFF
        
        if  key in [ord('q'), ord('x')]:
            break
        elif key == [ord('g')]:
            video = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('camara', video)
    else:
        break
cap.release()
cv2.destroyAllWindows()