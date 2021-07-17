import numpy as np
import cv2
import urllib.request
from src.Vision.QR_reader import getQRS
from math import sqrt

x=14 # largo de la caja patrón
y=4.1 # ancho de la caja patrón
dim1 = x/322.5 # centímetros por pixel
dim2 = y/107.1 # centímetros por pixel
dim1, dim2 = [1, 1]
def getPosNorm(img, xrect, yrect, W, H):
    result, pts= [], []
    for QR in getQRS(img): # considerando múltiples QR en una imagen
        wc, hc = QR['rect'].width, QR['rect'].height # dimensiones del QR
        Cx, Cy = 0, 0 # se inicializan coordenadas del centroide en 0
        for point in QR['polygon']: # se recorren los puntos del polígono del QR
            Cx += point.x
            Cy += point.y
        pts=np.array([[point.x, point.y] for point in QR['polygon']], np.int32).reshape((-1, 1, 2)) if QR['polygon'] else []
        Cx/=4; Cy/=4 # se obtiene el centroide absoluto en la imagen
        Cx-=xrect; Cy-=yrect # se obtienen coordenadas relativas al origen del rectángulo delimitador
        [xn,yn]=[Cx/W,Cy/H] # posición normalizada
        [wn,hn]=[wc/W,hc/H] # tamaño normalizado
        result.append({"x":xn,"y":yn,"w":wn,"h":hn}) # agregando el resultado a la lista
    return result, pts

def getContour(img):
    # convertir a escala de grises
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # thresholding binario
    _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)             
    image_copy = img.copy() # para dibujar sobre la imagen original
    c = max(contours, key = cv2.contourArea) # para obtener el contorno más grande
    x,y,w,h = cv2.boundingRect(c) # se aproxima a un rectángulo
    # se dibuja en verde el rect. aproximación, ya que la cámara apunta perpendicular al suelo
    box = cv2.convexHull(c)
    print(box)
    cv2.drawContours(image_copy,[box],0,(0,0,255),2)
    return image_copy, x, y, w, h

last_known_position=np.array([], np.int32)
while True:
    url = "http://192.168.100.75:8080/shot.jpg"
    imgResp=urllib.request.urlopen(url) 
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img=cv2.resize(img, (720, 480), interpolation = cv2.INTER_AREA)
    img, x, y, w, h= getContour(img)
    result, pts= getPosNorm(img, x, y, w, h)
    if len(pts): last_known_position = pts
    cv2.polylines(img, last_known_position, True, (255, 0, 0), 2) # quiero dibujar el QR pero aún no me sale
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        break
