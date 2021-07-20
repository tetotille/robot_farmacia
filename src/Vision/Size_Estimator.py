import numpy as np
import cv2
import urllib.request
from src.Vision.QR_reader import getQRS
from math import sqrt

x=9.6 # largo de la caja patrón
y=5.2 # ancho de la caja patrón
dim1 = x/275.0727176584403 # centímetros por pixel
dim2 = y/136.4734406395618 # centímetros por pixel
start_bound = [244, 88]
end_bound = [580, 400]

def getPosNorm(img):
    result, pts= [], []
    for QR in getQRS(img): # considerando múltiples QR en una imagen
        Cx, Cy = 0, 0 # se inicializan coordenadas del centroide en 0
        for point in QR['polygon']: # se recorren los puntos del polígono del QR
            Cx += point.x
            Cy += point.y
        pts=np.array([[point.x, point.y] for point in QR['polygon']], np.int32).reshape((-1, 1, 2)) if QR['polygon'] else []
        Cx/=4; Cy/=4 # se obtiene el centroide absoluto en la imagen
    return result, pts

def getContour(img):
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=6., tileGridSize=(8,8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different chann
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2,a,b))  # merge channels
    img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    cv2.imshow('Increased contrast', img2)
    #cv2.imwrite('sunset_modified.jpg', img2)
    # convertir a escala de grises
    img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    # thresholding binario
    _, thresh = cv2.threshold(img_gray, 90, 255, cv2.THRESH_BINARY)
    thresh[:,:start_bound[0]] = 0
    thresh[:,end_bound[0]:] = 0
    thresh[:start_bound[1],:] = 0
    thresh[end_bound[1]:,:] = 0
    # do connected components processing
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, None, None, None, 8, cv2.CV_32S)

    #get CC_STAT_AREA component as stats[label, COLUMN] 
    areas = stats[1:,cv2.CC_STAT_AREA]

    result = np.zeros((labels.shape), np.uint8)

    for i in range(0, nlabels - 1):
        if areas[i] >= 300:   #keep
            result[labels == i + 1] = 255
    cv2.imshow("filtrado", thresh)
    cv2.imshow("sin ruido", result)
    contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)             
    image_copy = img.copy() # para dibujar sobre la imagen original
    c = max(contours, key = cv2.contourArea) # para obtener el contorno más grande
    # se dibuja en verde el rect. aproximación, ya que la cámara apunta perpendicular al suelo
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(image_copy,[box],0,(0,0,255),2)
    box = [*box, box[0]]
    distances = [sqrt((box[i][0]-box[i+1][0])**2
                    + (box[i][1]-box[i+1][1])**2)
                    for i in range(4)]
    width = min(distances)*dim2
    length = max(distances)*dim1
    print(width, length)
    return image_copy

last_known_position=np.array([], np.int32)
while True:
    url = "http://192.168.100.75:8080/shot.jpg"
    imgResp=urllib.request.urlopen(url) 
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img=cv2.resize(img, (720, 480), interpolation = cv2.INTER_AREA)
    img= getContour(img)
    img= cv2.rectangle(img, start_bound, end_bound, (0, 255, 0), 2)
    result, pts= getPosNorm(img)
    if len(pts): last_known_position = pts
    cv2.imshow('test',img)
    if ord('q')==cv2.waitKey(10):
        break
