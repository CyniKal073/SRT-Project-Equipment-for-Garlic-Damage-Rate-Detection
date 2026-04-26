import cv2
import numpy
import time


#capture = cv2.VideoCapture(1)
capture1 = cv2.VideoCapture(0)
#t=0
while (True):
    #ret, frame = capture.read()
    ret1, frame1 = capture1.read()
    #frame = cv2.flip(frame, 1)
    #print(frame)
    #cv2.imshow('video', frame)
    cv2.imshow('video1', frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #print(1./(time.time()-t))
    #t = time.time()


cv2.destroyAllWindows()