import cv2
import numpy as np
from mqtt_class import mqtt
import utils
import signal
import os
import json

def sigint_handler(signum, frame):
    if signum == signal.SIGINT:
        logger.error( 'Kesme geldi programdan çıkılıyor...' )
    os.kill( os.getpid(), signal.SIGKILL )


# Logger ve sinyal ayarlandı
logger = utils.set_logger( __name__, __file__ )
logger.info( 'Kod Baslatildi' )
signal.signal( signal.SIGINT, sigint_handler )

### Ucretsiz MQTT Broker'ı uzerinde islemler yapilmasi için internet üzerinden free host(broker.emqx.io) kullanıldı 
mq=mqtt(broker="broker.emqx.io")
mq.connect()
cap = cv2.VideoCapture("video.mp4")
i=0
istasyon_no=1
while True:
    ret, frame = cap.read()
    reSize = frame[350:800,300:1400]
    blur = cv2.GaussianBlur(reSize, (5,5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    i=i+1
    low_yellow = np.array([18,94,140])
    up_yellow = np.array([48,255,255])
    low_brown = np.array([20,100,100])
    up_brown = np.array([30,255,255])
    mask_y = cv2.inRange(hsv, low_yellow, up_yellow)
    mask_r = cv2.inRange(hsv, low_brown, up_brown)
    mask = mask_r+mask_y

    edges = cv2.Canny(mask, 75, 158)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30, maxLineGap=50)


    if lines is not None:
        for line in lines:
            x, y, w, h = line[0]
            cv2.line(blur, (x, y), (w, h), (0,255,0), 4)
    if not ret:
        cap = cv2.VideoCapture("video.mp4")
        continue

    cv2.imshow("mask",mask)
    cv2.imshow("blur",blur)

    key = cv2.waitKey(25)
    if key == 27:
        break
    
    ### Yapilan islemler ile dogruluğu gorme icin yazdirildi
    if (i>1500 and i<1630) or (i>2500 and i<2650):
        logger.info("Hayati tehlike")
        mq.publish("hayati_tehlike",json.dumps({"istasyon_no":istasyon_no}))
    elif (i>1670 and i<2200):
        logger.info("Tren geldi")
        mq.publish("tren_ulasti",json.dumps({"istasyon_no":istasyon_no}))
    

cap.release()
cv2.destroyAllWindows()
