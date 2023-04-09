# importing the module
import cv2
import pickle


# function to display the coordinates of
# of the points clicked on the image
import numpy as np


def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    global rectangle
    global spots
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.circle(img,(x,y),3,(255,0,0),-1)
        cv2.imshow('image', img)
        rectangle.append((x,y))

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x, y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)
    if len(rectangle)==4:
        spots.append(rectangle)
        rectangle=[]
        print(spots)


# driver function
global rectangle
global spots
spots=[]
rectangle=[]
if __name__ == "__main__":
    # reading the image
    img = cv2.imread('parking_footage/vlc.png', 1)

    # displaying the image
    cv2.imshow('image', img)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    if cv2.waitKey(0) & 0xFF == ord('q'):
        print(spots)
        with open('parking_spots_3.pickle', 'wb') as f:
            pickle.dump(spots, f)
    # close the window
    cv2.destroyAllWindows()