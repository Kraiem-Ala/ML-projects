import os
import pickle
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
from mrcnn import model, config, visualize, utils
import cv2
from shapely.geometry import Polygon

def displayImage(img, feed):
    qformat = QImage.Format_RGB888
    img = QImage(img, img.shape[1], img.shape[0], qformat)
    img = img.rgbSwapped()
    feed.setPixmap(QPixmap.fromImage(img))


class simple_config(config.Config):
    NAME = "cars_cfg"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    NUM_CLASSES = 2


class detetion_mod:
    def __init__(self):
        file = open('parking_spots_3.pickle', 'rb')
        self.parking_spots = pickle.load(file)
        self.num_parking_spots = len(self.parking_spots)
        file.close()
        self.test_model = model.MaskRCNN(mode="inference", config=simple_config(), model_dir=os.getcwd())
        self.test_model.load_weights(filepath="cars_model.h5", by_name=True)
        self.class_names = ['back_ground', 'car']

    def draw_polygon(self, img, rect, color):
        cv2.line(img, rect[0], rect[1], color, 2)
        cv2.line(img, rect[1], rect[2], color, 2)
        cv2.line(img, rect[2], rect[3], color, 2)
        cv2.line(img, rect[3], rect[0], color, 2)

    def overlap(self, cars_boxes, parking_boxes, img):
        color = (0, 255, 0)
        parked = False
        for i, park in enumerate(parking_boxes):
            color = (0, 255, 0)
            park_area = Polygon(park)
            park_area_size = park_area.area
            for car in cars_boxes:
                y1 = car[0]
                x1 = car[1]
                y2 = car[2]
                x2 = car[3]

                p1 = (x1, y1)
                p2 = (x2, y1)
                p3 = (x2, y2)
                p4 = (x1, y2)
                cars = [p1, p2, p3, p4]
                car_area = Polygon(cars)
                intersection_area = car_area.intersection(park_area).area
                if (intersection_area / park_area_size) >= 0.25:
                    parked = True
                    color = (0, 0, 255)
                    break
            self.draw_polygon(img, park, color)

    def detection(self, iterartions, feed,ui_window):
        vid = cv2.VideoCapture('parking_footage/footage 3.mp4')
        iterat = 0
        while (iterat < iterartions):
            ret, frame = vid.read()
            iterat += 1
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image2 = np.copy(image)
            # Detect results
            r = self.test_model.detect([image])[0]
            cars_boxes = r["rois"]
            self.overlap(cars_boxes, self.parking_spots, image)
            """visualize.display_instances(image=image,boxes=r['rois'],masks=r['masks'],class_ids=r['class_ids'],class_names=class_names,scores=r['scores'])"""
            object_count = len(r["class_ids"])
            for i in range(object_count):
                box = r["rois"][i]
                y1, x1, y2, x2 = box
                cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 1, cv2.LINE_4)
                mask = r["masks"][:, :, i]
                image2[mask] = [200, 100, 0]
            added_image = cv2.addWeighted(image, 1.0, image2, 0.4, 0)
            displayImage(added_image, feed)
            ui_window.set_parkings_numbers(self.num_parking_spots)
            ui_window.set_occupied_numbers(object_count)
            ui_window.set_free_numbers(self.num_parking_spots-object_count)
            cv2.waitKey(10)