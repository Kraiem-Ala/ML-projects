import numpy as np
from grabscreen import grab_screen
import cv2
import time
from getkey import key_check
import os
import keyboard

def keys_to_output(keys):
    """
    Convert keys to a ...multi-hot... array

    [Q,Z,D] boolean values.
    """
    output = [0, 0, 0]

    if 'Q' in keys:
        output[0] = 1
    elif 'D' in keys:
        output[2] = 1
    else:
        output[1] = 1
    return output


file_name = 'training_data_1.npy'

if os.path.isfile(file_name):
    print('File exists, loading previous data!')
    training_data = list(np.load(file_name,allow_pickle=True))
else:
    print('File does not exist, starting fresh!')
    training_data = []


def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    while (True):
        # 800x600 windowed mode
        screen = grab_screen(region=(0,35,1280,650))
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # resize to something a bit more acceptable for a CNN
        screen = cv2.resize(screen, (80, 60))
        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen, output])
        #cv2.imshow("screen",screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        if keyboard.is_pressed('b'):
            print(len(training_data))
            np.save(file_name, training_data)
            break
        if len(training_data) % 500 == 0:
            print(len(training_data))
            np.save(file_name, training_data)
if __name__ == '__main__':
    main()