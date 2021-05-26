import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor


widgets = {
        "logo": [],
        "button": []
    }

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Mecabot - Bienvenido")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #91BEF7;")

grid = QGridLayout()

def frame1():
    #display Logo
    image = QPixmap("img/logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top:50px; margin-bottom:50px")
    widgets["logo"].append(logo)
    
    #button widget
    button = QPushButton("Escanear Código QR")
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
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0)
    grid.addWidget(widgets["button"][-1], 1, 0)


frame1()

window.setLayout(grid)

window.show()
sys.exit(app.exec())
