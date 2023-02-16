import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
x_medium = 320
y_medium = 240
x = 0
y = 0

def qr_Algilama():

    while True:
        success, img = cap.read()
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            print(myData)
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0,255,255), 5)
            (x, y, w, h) = cv2.boundingRect(pts)
            x_medium = int((x+x+w) / 2)
            y_medium = int((y+y+h) / 2)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 4)
            break
        cv2.line(img, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
        cv2.line(img, (0, y_medium), (680, y_medium), (255, 0, 0), 2)
        cv2.imshow('Result', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
        x_medium = 320
        y_medium = 240
cap.release()
cv2.destroyAllWindows()