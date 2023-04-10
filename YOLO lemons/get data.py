import cv2
import os
cap = cv2.VideoCapture('lemons.mp4')
count=0
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    os.chdir('C:/Users/Kraiem Ala Eddine/Desktop/Machine learning tuto/ML-project/YOLO lemons/train')
    if ret == True:
        frame=cv2.resize(frame,(512,512),interpolation = cv2.INTER_AREA)
        cv2.imshow('Frame',frame)
        if cv2.waitKey(0) & 0xFF == ord('s'):
            count+=1
            cv2.imwrite('lemons'+str(count)+'.png',frame)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
