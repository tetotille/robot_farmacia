import sys
from src.Vision.QR_reader import *
from src.data import data_handler
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

root_path = "./src/GUI"

# Dirección del ARDUINO
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.2)

# URL DE LA PRIMERA CAMARA: camara de pedidos
url = "http://192.168.100.43:8080/shot.jpg"

# URL DE LA SEGUNDA CAMARA: camara de reposición
url_repo = "http://192.168.400.3:8080/shot.jpg"

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
        frame de espera o al frame principal con el botón volver.
        
        Al detectar el medicamento envía un mensaje al arduino con la ubicación del
        medicamento que se tomará.

        El QR tiene como formato: ID:medicamento:cantidad
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
        button1 = createButton("Volver")
        button1.clicked.connect(frame1)
        QtTest.QTest.qWait(50)
        
        # Comunicación con ARDUINO
        # Condición de medicamento detectado, se retira el medicamento que se encontró en el QR
        if qr != []:
            if alerta(first_qr['text'])==1024:
                # una vez que se encuentra el medicamento se debe de decir el lugar donde está
                # y mandar eso al arduino
                ID = first_qr.split(":")[0]
                # buscar_medicamento le tiene que dar la posición del rack por ahí que estaría
                # enumerado del 0 al 15
                medicamento_detectado = data_handler.search_box(ID) # ATENCION si es None
                if medicamento_detectado is not None:
                    frame_sin_medicamento()
                    arduino.write(encode(medicamento_detectado+"\n", 'UTF-8'))
                break
            else: continue
    show_frame_espera()


def frame1():
    """
    Frame de pantalla principal

    Aparece el logo y dos botones:
        --------------
        |   MECABOT  |
        --------------
        -Escanear código QR
        -Listar los medicamentos disponibles
    """
    global ocupado, arduino, bandera
    bandera = False
    clear_widgets()
    #display Logo
    image = QPixmap(f"{root_path}/img/logo.png")
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
    
    # Verifica si se apretó el botón de reposición - Comunicación con ARDUINO
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
        frame_espera(1, msg="El robot está trayendo su pedido.")
        
        # Condición de salida - Comunicación con ARDUINO
        salida = arduino.readline().decode() == "retirar\n"
        if salida == True:
            break
        
        QtTest.QTest.qWait(500)
        frame_espera(2, msg="El robot está trayendo su pedido.")
        
        # Condición de salida - Comunicación con ARDUINO
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
    

def frame_espera(logo_espera, msg):
    clear_widgets() # primero se limpia
    #accion es un booleano que especifica si va a esperar o no
    image = QPixmap(f"{root_path}/img/{logo_espera}.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje(msg)
    
    widgets["logo"].append(logo)
    grid.addWidget(widgets["logo"][-1], 0, 0)
    widgets["message"].append(mensaje)
    grid.addWidget(widgets["message"][-1], 1, 0)

def deteccion_qr(url2, bandera_qr):
    global arduino
    
    # Detección QR
    imgResp = urllib.request.urlopen(url2)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgNp, -1)
    qr = getQRS(img)
    first_qr = qr[0] if qr else {} # se asume solo un QR en la imagen

    if qr and bandera_qr:
        bandera_qr = 0
        ID = first_qr.split(":")[0]
        medicamento_detectado = data_handler.save_box(ID) # ATENCION si es None
        if medicamento_detectado is not None:
            print(qr) # reemplazar
            arduino.write(encode(medicamento_detectado+"\n", 'UTF-8'))

    QtTest.QTest.qWait(100) # OJO
    data = arduino.readline().decode()
    return bandera_qr, data

def show_frame_espera_2():
    bandera_qr = 1
    while(True):
        frame_espera(3, msg="Mecabot está ocupado, por favor espere.")
        bandera_qr, data = deteccion_qr(url_repo, bandera_qr)
        print(data)

        frame_espera(4, msg="Mecabot está ocupado, por favor espere.")
        bandera_qr, data = deteccion_qr(url_repo, bandera_qr)
        print(data)

        # Condición de salir del frame de espera
        if data == "desocupado\n": break
    start_program()
    
    
def frame_retirar():
    """
        Imprime un mensaje en pantalla para retirar el medicamento una vez que
        llega a la caja de donde se puede agarrar, el mensaje dura 4 segundos
        y luego vuelve a la pantalla principal.
    """
    image = QPixmap(f"{root_path}/img/fin.png")
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


def frame_sin_medicamento():
    """
        Imprime un mensaje en pantalla que no se encuentra el medicamento,
        el mensaje dura 4 segundos y luego vuelve a la pantalla principal.
    """
    image = QPixmap(f"{root_path}/img/not_found.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    
    mensaje = crear_mensaje("Medicamento fuera de stock.")
    
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
    image = QPixmap(f"{root_path}/img/logo.png")
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
