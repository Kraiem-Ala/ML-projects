import pickle
import cv2


def draw_polygon(img, rect,i):
    cv2.line(img, rect[0], rect[1], (0, 255, 0), 2)
    cv2.line(img, rect[1], rect[2], (0, 255, 0), 2)
    cv2.line(img, rect[2], rect[3], (0, 255, 0), 2)
    cv2.line(img, rect[3], rect[0], (0, 255, 0), 2)
    cv2.putText(img,str(i),rect[0],cv2.FONT_ITALIC,1,(255,0,0),1)


if __name__ == "__main__":
    # open a file, where you stored the pickled data
    file = open('parking_spots.pickle', 'rb')

    # dump information to that file
    data = pickle.load(file)
    file.close()

    img = cv2.imread("parking_footage/22.png")
    for i,cnt in enumerate(data):
        draw_polygon(img, cnt,i)
    cv2.imshow("spots", img)
    cv2.waitKey(0)
