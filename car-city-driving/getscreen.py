from PIL import ImageGrab
import numpy as np
import time
import cv2
import keyboard
thresh1=100
thresh2=250
import pyautogui
import pydirectinput
def draw_lines(img,lines):
    a1 = 0
    a2 = 0
    biases=[]
    weights=[]
    try :
        # for line in lines:
        #     coords = line[0]
        #     #cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,0], 3)
        #     a=round((coords[1] - coords[3])/(coords[0] - coords[2]),4)
        #     b = coords[1]-coords[0]*a
        #     if len(biases)==0:
        #         biases.append(a)
        #         weights.append(b)
        #         cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 0], 3)
        #     elif len(biases)==1:
        #         biases.append(a)
        #         weights.append(b)
        #         cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 0], 3)
        line1=lines[0]
        coords = line1[0]
        a1 = round((coords[1] - coords[3]) / (coords[0] - coords[2]), 4)
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 0], 3)
        line2 = lines[-1]
        coords = line2[0]
        a2 = round((coords[1] - coords[3]) / (coords[0] - coords[2]), 4)
        cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255, 255, 0], 3)

    except:
        #print("none")
        pass
    return a1,a2
def roi(img, vertices):
    mask = np.zeros_like(img)
    # fill the mask
    cv2.fillPoly(mask, vertices, 255)
    # now only show the area that is the mask
    masked = cv2.bitwise_and(img, mask)
    return masked

def process_image(original_image):
    processed_image = cv2.cvtColor(original_image,cv2.COLOR_RGB2GRAY)
    #yprocessed_image= cv2.Canny(processed_image,threshold1=thresh1, threshold2=thresh2)
    _, processed_image = cv2.threshold(processed_image, 254, 255, cv2.THRESH_BINARY)
    #blur = cv2.GaussianBlur(processed_image, (5, 5), 0)
    vertices = np.array([[0, 470], [610, 375], [715, 375], [1280, 518],], np.int32)
    processed_image = roi(processed_image, [vertices])
    # processed_image2 = roi(blur, [vertices])
    lines = cv2.HoughLinesP(processed_image, 1, np.pi /180, 10, np.array([]), 100, 100)
    a1,a2=draw_lines(processed_image, lines)
    return processed_image,a1,a2
def detect_points(img):
    points=[]
    index = 0
    j=0
    for line in img :
        for i in range(len(line)):
            if img[j][i]==255:
                if index <2:
                    point=(i,j)
                    points.append(point)
                    index+=1
                else:
                    break
        j+=1
    print(points)
    cv2.line(img, points[0], points[1], [255, 255, 0], 3)
def forward():
    pyautogui.keyDown('z')
def right():
    pyautogui.keyDown('d')
    pyautogui.keyUp('z')
def left():
    pyautogui.keyDown('q')
    pyautogui.keyUp('z')
def stop():
    pyautogui.keyUp('z')
    pyautogui.keyDown('s')
    time.sleep(0.2)
    pyautogui.keyUp('s')
def start_proc():
    time.sleep(4)
    print("Seat belt ON")
    pyautogui.keyDown('y')
    time.sleep(0.5)
    pyautogui.keyUp('y')
    print("strating engine")
    pyautogui.keyDown('e')
    time.sleep(0.5)
    pyautogui.keyUp('e')
    pyautogui.keyDown('s')
    time.sleep(0.1)
    pyautogui.keyDown('shift')
    time.sleep(0.2)
    pyautogui.keyUp('shift')
    time.sleep(0.2)
    pyautogui.keyDown('shift')
    time.sleep(0.2)
    pyautogui.keyUp('shift')
    time.sleep(0.2)
    pyautogui.keyDown('shift')
    time.sleep(0.2)
    pyautogui.keyUp('shift')
    pyautogui.keyUp('s')
    pyautogui.keyDown('space')
    time.sleep(0.25)
    pyautogui.keyUp('space')
def stop_proc():
    pyautogui.keyDown('s')
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    time.sleep(0.2)
    pyautogui.keyDown('ctrl')
    time.sleep(0.2)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('s')
    pyautogui.keyDown('space')
    time.sleep(0.5)
    pyautogui.keyUp('space')
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')
    pyautogui.keyDown('y')
    pyautogui.keyUp('y')

start_proc()
while(True):
    screenshot = np.array(ImageGrab.grab(bbox=(0,35,1280,650)))
    new_screen,a1,a2 = process_image(screenshot)
    cv2.imshow('window',new_screen)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    if abs(a1+a2)<1:
        print("forward",abs(a1+a2))
        forward()
    elif a1+a2 < - 1:
        print("right", (a1+a2))
        right()
    elif a1+a2 > 1:
        print("left", (a1+a2))
        left()
    print(a1,a2)
stop()
stop_proc()
