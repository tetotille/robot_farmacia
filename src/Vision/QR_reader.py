import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(600, 400, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


def getQRS(img):
    return [{
        'polygon': QR.polygon,
        'rect': QR.rect,
        'text': QR.data.decode('utf-8')
    }
        for QR in pyzbar.decode(img)]


# cap = cv2.VideoCapture('http://192.168.100.41:8080')
# url = "http://192.168.100.41:8080/shot.jpg"



            
