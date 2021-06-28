import sys
from QR_reader import *
import urllib.request
import cv2
import numpy as np
from pyzbar import pyzbar
from data import *

from PyQt5.QtWidgets import (
                            QApplication, 
                            QLabel, 
                            QPushButton, 
                            QVBoxLayout, 
                            QWidget, 
                            QFileDialog, 
                            QGridLayout, 
                            QMessageBox, 
                            QListWidget,
                            QListWidgetItem,
                            )

from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5 import QtTest

import serial
# Para usar la biblioteca serial se debe utilizar el sudo python
# Desde Ubuntu con miniconda3 se debe hacer de la siguiente forma:

# sudo ~/miniconda3/envs/"ENVIRONMENT NAME"/bin/python3 qtpy.py

# Dirección del ARDUINO
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.2)

# URL DE LA PRIMERA CAMARA: camara de pedidos
url = "http://192.168.100.43:8080/shot.jpg"

# URL DE LA SEGUNDA CAMARA: camara de reposición
url_repo = "http://192.168.100.3:8080/shot.jpg"

#lista_medicamentos: la lista de todos los medicamentos disponibles

ocupado = False
bandera = False

widgets = {
        "logo": [],
        "button": [],
        "qrshow":[],
        "message":[],
        "lists":[]
    }

salida = False

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Mecabot - Bienvenido")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #91BEF7;")

grid = QGridLayout()


def crear_mensaje(msj):
    mensaje = QLabel(msj)
    mensaje.setAlignment(QtCore.Qt.AlignCenter)
    mensaje.setStyleSheet(
        '''
        font-size: 25px;
        font-style: Bold;
        '''
    )
    return mensaje


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


def alerta(medicamento):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("¿Usted está seguro que desea este medicamento?")
    msg.setInformativeText("Cuando presione 'Ok' se procederá a traerle "+ str(medicamento))
    msg.setWindowTitle("¿Está seguro?")
    msg.setDetailedText("")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    retval = msg.exec_()
    return retval


def frame_QR():
    """
        Muestra la cámara en la pantalla principal para que la persona pueda poner
        el código QR donde corresponde y luego cuando detecta el código le aparece
        un mensaje emergente que debe de aceptar para que se busque el medicamento
        indicado.
        
        Puede ser llamado a través del frame1 (pantalla principal) y luego va al
        frame de espera.
        
        Al detectar el medicamento envía un mensaje al arduino con la ubicación del
        medicamento que se tomará.
    """
    global url,bandera,arduino,lista_medicamentos
    bandera = True
    while True:
        # Se hace la detección del código QR y se guarda en qr
        clear_widgets()
        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        qr = getQRS(img)
        print(qr)
        # Se supone que hay un solo qr en la imagen
        first_qr = qr[0] if qr else {}
        
        small = cv2.resize(img, (0,0), fx=0.3, fy=0.3) 
        smallqt = convert_cv_qt(window,small)
        
        # Muestra cada pantallazo
        qrshow = QLabel()
        qrshow.setPixmap(smallqt)
        qrshow.setAlignment(QtCore.Qt.AlignCenter)
        qrshow.setStyleSheet("margin-top:50px; margin-bottom:50px")
        widgets["qrshow"].append(qrshow)
        grid.addWidget(widgets["qrshow"][-1], 1, 0)
        QtTest.QTest.qWait(50)
        
        # Condición de medicamento detectado, se guarda el medicamento que se encontró en el QR
        if qr != []:
            if alerta(first_qr['text'])==1024:
                # una vez que se encuentra el medicamento se debe de decir el lugar donde está
                # y mandar eso al arduino
                medicamento_detectado = buscar_medicamento(first_qr['text'])+"\n"
                arduino.write(encode(medicamento_detectado, 'UTF-8'))
                break
            else: continue
    show_frame_espera()


def frame1():
    global ocupado, arduino, bandera
    bandera = False
    clear_widgets()
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
    button2.clicked.connect(show_frame_listar)
    
    widgets["button"].append(button1)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)
    widgets["button"].append(button2)
    grid.addWidget(widgets["button"][-1], 2, 0)
    
    # Verifica si se apretó el botón
    while True:
        data = arduino.readline().decode()
        
        if bandera:
            break
        print(data)
        if data == "ocupado\n":
            break
        QtTest.QTest.qWait(500)
    if data == "ocupado\n":
        show_frame_espera_2()
    
def frame_espera1():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/1.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("El robot está trayendo su pedido.")
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)

def frame_espera2():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/2.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("El robot está trayendo su pedido.")
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)    

def show_frame_espera():
    """
        Este frame se encarga de mostrar la animación de espera
        mientras el robot trae el medicamento.
        
        Mientras que muestra los frames espera la palabra clave
        del arduino a través de UART, lo decodifica y lo compara
        y cuando al fin lo recibe muestra el frame de retirar
        medicamento.
    """
    global salida
    n=0
    while(True):
        clear_widgets()
        frame_espera1()
        
        # Condición de salida - Comunicación con Arduino
        salida = arduino.readline().decode() == "retirar\n"
        if salida == True:
            break
        
        QtTest.QTest.qWait(500)
        clear_widgets()
        frame_espera2()
        
        # Condición de salida - Comunicación con Arduino
        salida = arduino.readline().decode() == "retirar\n"
        if salida == True:
            break
        
        QtTest.QTest.qWait(500)
    frame_retirar()


def show_frame_listar():
    clear_widgets()
    frame_listar()


def frame_listar():
    
    global lista_medicamentos, bandera
    bandera = True
    
    mensaje = crear_mensaje("Aquí se muestran todos los medicamentos disponibles")
    
    lista = QListWidget()
    [lista.addItem(QListWidgetItem(str(medicamento))) for medicamento in lista_medicamentos]
    lista.setStyleSheet(
        '''
        font-size: 16px;
        padding: 25px;
        border: 2px solid #008CBA;
        border-radius: 10px;
        '''
    )
    
    button = createButton("Volver")
    button.clicked.connect(start_program)
    
    
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 0, 1)
    widgets["lists"].append(lista)
    grid.addWidget(widgets["lists"][-1], 1, 1)
    widgets["button"].append(button)
    grid.addWidget(widgets["button"][-1], 2, 1)
    

def frame_espera3():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/3.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("Mecabot está ocupado, por favor espere.")
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)

def frame_espera4():
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap("img/4.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("Mecabot está ocupado, por favor espere.")
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)    

def show_frame_espera_2():
    global salida, arduino
    n=0
    while(True):
        clear_widgets()
        frame_espera3()
        QtTest.QTest.qWait(100)
        clear_widgets()
        data = arduino.readline().decode()
        frame_espera4()
        QtTest.QTest.qWait(100)
        salida = n>4
        n+=1
        
        data = arduino.readline().decode()
        print(data)
        if data == "desocupado\n":
            break
    start_program()
    
    
def frame_retirar():
    """
        Imprime un mensaje en pantalla para retirar el medicamento una vez que
        llega a la caja de donde se puede agarrar, el mensaje dura 4 segundos
        y luego vuelve a la pantalla principal.
    """
    image = QPixmap("img/fin.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("Por favor retire su medicamento.")
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)
    QtTest.QTest.qWait(4000)
    start_program()

def start_program():
    clear_widgets()
    frame1()


def frame_base():
    #display Logo
    image = QPixmap("img/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:80px")
    widgets["logo"].append(logo)
    
    #button widget
    button1 = createButton("Iniciar Mecabot")
    button1.clicked.connect(start_program)
    
    widgets["button"].append(button1)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)
    
    
frame_base()

window.setLayout(grid)

window.show()

app.exec()
