import torch
import cv2
from PIL import Image
import pandas
cap = cv2.VideoCapture("YOLO lemons/lemons.mp4")
constructors=["Yellow lemon","Green lemon"]
colors=[(0,0,102),(255,150,0)]
model = torch.hub.load("yolov5", 'custom', path="yolov5/runs/train/exp/weights/best.pt", source='local')

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = model(im_rgb)
        for obj in result.xyxy[0]:
            if obj[4] > 0.0:
                classe = int(obj[5])
                im_rgb = cv2.rectangle(im_rgb, (int(obj[0]), int(obj[1])), (int(obj[2]), int(obj[3])), colors[classe],2, 2)
                im_rgb = cv2.putText(im_rgb, constructors[classe], (int(obj[0]), int(obj[1]) - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors[classe], 1, cv2.LINE_4)
        # print(result.pandas().xyxy[0])
        # result.show()
        im = cv2.cvtColor(im_rgb, cv2.COLOR_RGB2BGR)
        im=cv2.resize(im,(512,512),interpolation = cv2.INTER_AREA)
        frame=cv2.resize(frame,(512,512),interpolation = cv2.INTER_AREA)
        cv2.imshow("test_img", im)
        cv2.imshow("test_img2", frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break



