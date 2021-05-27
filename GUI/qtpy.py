import sys
from QR_reader import *
import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5 import QtTest




widgets = {
        "logo": [],
        "button": [],
        "qrshow":[]
    }

salida = False


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Mecabot - Bienvenido")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #91BEF7;")

grid = QGridLayout()


def clear_widgets():
    for widget in widgets:
        for i in range(0, len(widgets[widget])):
            if widgets[widget] != []:
                widgets[widget][-1].hide()
            widgets[widget].pop()


def createButton(words):
    button = QPushButton(words)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{background-color: white;
        border: 2px solid #008CBA; /* Blue */
        color: black;
        padding: 25px 0px;
        font-style: Ubuntu;
        text-align: center;
        text-decoration: none;
        font-size: 16px;}
        *:hover
        {
            background-color: #008CBA; /* Blue */
            color: white;
        }
        '''
    )
    return button


def frame_QR():
    url = "http://192.168.100.3:8080/shot.jpg"
    while True:
        clear_widgets()
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        qr = getQRS(img)
        print(qr)
        small = cv2.resize(img, (0,0), fx=0.3, fy=0.3) 
        smallqt = convert_cv_qt(window,small)
        
        qrshow = QLabel()
        qrshow.setPixmap(smallqt)
        qrshow.setAlignment(QtCore.Qt.AlignCenter)
        qrshow.setStyleSheet("margin-top:50px; margin-bottom:50px")
        widgets["qrshow"].append(qrshow)
        grid.addWidget(widgets["qrshow"][-1], 1, 0)
        QtTest.QTest.qWait(50)
        if qr != []:
            show_frame_espera()


def frame1():
    #display Logo
    image = QPixmap("img/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    widgets["logo"].append(logo)
    
    #button widget
    button1 = createButton("Escanear código QR")
    button2 = createButton("Listar los medicamentos disponibles")
    button1.clicked.connect(frame_QR)
    
    widgets["button"].append(button1)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)
    widgets["button"].append(button2)
    grid.addWidget(widgets["button"][-1], 2, 0)
    
def frame_espera1():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/1.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)

def frame_espera2():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/2.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
        

def show_frame_espera():
    global salida
    n=0
    while(True):
        clear_widgets()
        frame_espera1()
        QtTest.QTest.qWait(500)
        clear_widgets()
        frame_espera2()
        QtTest.QTest.qWait(500)
        salida = n>4
        n+=1
        if salida == True:
            start_program()

def start_program():
    clear_widgets()
    frame1()
    

start_program()

window.setLayout(grid)

window.show()
sys.exit(app.exec())
