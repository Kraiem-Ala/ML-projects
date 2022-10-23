import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkey import key_check
import os
import pyautogui
from alexnet_2 import alexnet

WIDTH = 80
HEIGHT = 60
LR = 1e-3
EPOCHS = 8
MODEL_NAME = 'city-car-1-{}-{}-{}-epochs.model'.format(LR, 'alexnetv2', EPOCHS)


def forward():
    pyautogui.keyDown('z')
    pyautogui.keyUp('q')
    pyautogui.keyUp('d')


def right():
    pyautogui.keyUp('q')
    pyautogui.keyDown('d')
    pyautogui.keyDown('z')
    time.sleep(0.2)
    pyautogui.keyUp('d')


def left():
    pyautogui.keyUp('d')
    pyautogui.keyDown('q')
    pyautogui.keyDown('z')
    time.sleep(0.2)
    pyautogui.keyUp('q')



def stop():
    pyautogui.keyUp('z')
    pyautogui.keyDown('s')
    time.sleep(0.5)
    pyautogui.keyUp('s')


model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while (True):

        if not paused:
            # 800x600 windowed mode
            screen = grab_screen(region=(0, 35, 1280, 650))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (80, 60))
            prediction = model.predict([screen.reshape(80, 60, 1)])[0]
            moves = list(np.around(prediction))
            print(moves,prediction)
            if moves == [1, 0, 0]:
                left()
            elif moves == [0, 1, 0]:
                forward()
            elif moves == [0, 0, 1]:
                right()

        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                pyautogui.keyUp('z')
                pyautogui.keyUp('q')
                pyautogui.keyUp('d')
                stop()
                time.sleep(0.5)
        elif 'P' in keys:
            break

main()