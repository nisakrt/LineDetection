import cv2
import numpy as np

cap = cv2.VideoCapture("video.mp4")

while True:
    ret, frame = cap.read()
    reSize = frame[350:800,300:1400]
    blur = cv2.GaussianBlur(reSize, (5,5), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

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

cap.release()
cv2.destroyAllWindows()
