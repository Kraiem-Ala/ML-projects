import cv2
import os
for count, filename in enumerate(os.listdir('.')):
    im=cv2.imread(filename)
    cv2.imshow('image',im)
    if cv2.waitKey(0)&0xFF==ord('q'):
        pass
    im=cv2.resize(im,(10,10),interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{filename}",im)