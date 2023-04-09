from PyQt5.QtWidgets import QMainWindow , QApplication, QLabel,QWidget,QProgressBar,QSplitter,QLCDNumber,QMenuBar, QCheckBox
from PyQt5 import uic
from cars_detection import *
import sys
class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi("dashboard.ui",self)
        self.total_number = self.findChild(QLCDNumber,"lcdNumber_4")
        self.occupied = self.findChild(QLCDNumber, "lcdNumber")
        self.free = self.findChild(QLCDNumber, "lcdNumber_2")
        self.illegal = self.findChild(QLCDNumber, "lcdNumber_3")
        self.progress = self.findChild(QProgressBar,"capacity_bar")
        self.feed = self.findChild(QLabel,"live_feed")
        self.start = self.findChild(QCheckBox, "start")
        self.start.stateChanged.connect(self.start_hundler)
        self.detector = detetion_mod()
        self.show()

    def start_hundler(self):
        self.detector.detection(200, self.feed, self)
    def set_parkings_numbers(self, number):
        self.total_number.display(number)
    def set_occupied_numbers(self, number):
        self.occupied.display(number)
    def set_free_numbers(self, number):
        self.free.display(number)
    def set_illegal_numbers(self, number):
        self.illegal.display(number)
    def set_progress_bar(self, percent):
        self.progress.setValue(percent)

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()