import time
import numpy as np
import cv2
import serial
import os
import glob
import sys
from mss import mss
from PIL import Image
import time

########################################### variables ######################################################
arduino = serial.Serial(port='COM5', baudrate=2000000, timeout=.001)
video = "C:\\Users\\james\\Desktop\\Hackathon_2023\\Videos\\AK-74U.mp4"
cap = cv2.VideoCapture(video)
# bbox for shells
bbox = [595, 100, 585, 480]
# bounding box for hands (gun type detection)
bbox_hand = [497, 435, 288, 285]
xb, yb, wb, hb = bbox
xh, yh, wh, hh = bbox_hand
# lower and upper hsv bounds for shell detection
shell_low = np.array([17, 78, 101])
shell_up = np.array([255, 255, 255])
# lower and upper hsv bounds for weapon detection
hand_low = np.array([10, 25, 122])
hand_up = np.array([18, 154, 235])
# lower and upper bounds for death detection
lower_red = np.array([0, 100, 100])  # Lower bound for red in HSV
upper_red = np.array([10, 255, 255])  # Upper bound for red in HSV
############################################## functions ####################################################
def write_to_arduino(message):
   try:
      arduino.write(bytes(message, 'utf-8'))
      return True
   except:
      print("Serial communication error!")
      return False


x_frame,y_frame,w_frame,h_frame = 3002,0,900,900
def select_region():
    sct = mss()
    monitor = {'top': y_frame, 'left': x_frame, 'width': w_frame, 'height': h_frame}
    img = Image.frombytes('RGB', (w_frame, h_frame), sct.grab(monitor).rgb)
    image_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    bbox = cv2.selectROI("tracking", image_cv2, fromCenter=False, showCrosshair=True)

    cv2.destroyAllWindows()
    x, y, width, height = bbox
    return x + x_frame, y + y_frame, width, height
#print(select_region())

# Initialize a list to store the centroids' x-coordinates
centroid_positions = []
# use to look for a shot for a certain number of frames
delay_cnt = 0
# Initialize a variable to track barrier crossing

while True:
    # # # # # # # # # # # # # # # # # # # # #  # ##  ## # Computer vision part ## # #  # #  # # # # # # #
    # capture frame
    #ret, frame = cap.read()
    sct = mss()
   # bbox = select_region()
    monitor = {'top': x_frame, 'left': y_frame, 'width': w_frame, 'height': h_frame}
    img = Image.frombytes('RGB', (w_frame, h_frame), sct.grab(monitor).rgb)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    initial = time.time()
    data_str = None
    if (arduino.inWaiting() > 0):
        # read the bytes and convert from binary array to ASCII
        data_str = arduino.read(1)
        data_str = str(data_str)
    if data_str is not None and "1" in data_str or delay_cnt > 0:
        if data_str is not None and "1" in data_str:
            delay_cnt = 20
        else:
            delay_cnt = delay_cnt -1
        #time.sleep(0.008)
        # convert frame to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # apply hsv masking
        mask_shell = cv2.inRange(hsv, shell_low, shell_up)
        mask_hand = cv2.inRange(hsv, hand_low, hand_up)
        death_mask = cv2.inRange(hsv, lower_red, upper_red)
        # Find contours in the mask
        contours_death, _ = cv2.findContours(death_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Extract ROIs directly from the HSV frame
        roi_shell = mask_shell[yb:yb+hb, xb:xb+wb]
        roi_hand = mask_hand[yh:yh+hh, xh:xh+wh]
        # grab contours from masks
        contours, _ = cv2.findContours(roi_shell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        contours_hand, _ = cv2.findContours(roi_hand, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # draw barrier line
        barrier = cv2.line(frame, (xb + int(wb/2), yb + hb), (xb+int(wb/2), yb + 150), (155, 12, 25), 4)
        barrier_crossed = False
        gun_type = None
        # Check if centroids have crossed the barrier
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            if area > 200 or w > 60 or h > 60:
                x, y = x + xb, y + yb
                centroid_x = x + w // 2
                centroid_y = y + h // 2
                perimeter = 2 * w + 2 * h
                if perimeter > 55:
                    perimeter = 1
                if barrier_crossed == True and x + 11 < xb + int(wb/2):
                    barrier_crossed = False
                time.sleep(0.01)
                # detect a shell crossing the line for a "shot"
                if x - 11 < xb + int(wb/2) and x + w + 10 > xb + int(wb/2) or barrier_crossed == True:
                    barrier_crossed = True
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (234, 193, 79), 2)
                    time.sleep(0.05)
                    cv2.circle(frame, (centroid_x, centroid_y), 5, (2, 255, 0), -1)
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 225), 2)
                    cv2.circle(frame, (centroid_x, centroid_y), 5, (2, 0, 255), -1)
        # weapon discovering: looks for hand area to decide if user is using a handgun.
        for contour in contours_hand:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            offset_contour = contour + (xh, yh)
            # if massive hand mask area then most likely a handgun
            if area > 28000:
                cv2.drawContours(frame, [offset_contour], -1, (0, 255, 0), 2)
                cv2.putText(frame, "Handgun", (490, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (112, 255, 0), 1)
                gun_type = "Handgun"
        if gun_type == "Handgun" and barrier_crossed:
            print("Firing Handgun!")
            #write_to_arduino(9)
        elif barrier_crossed:
            print("Firing Rifle")
            #write_to_arduino(556)
        total_contour_area = 0
        for contour in contours_death:
            total_contour_area += cv2.contourArea(contour)
        if total_contour_area > 330516:
            print("DIED")
            write_to_arduino(44)
        # do all the drawing functions
        cv2.rectangle(frame, (xb, yb), (xb + wb, yb + hb), (0, 255, 0), 2)
        cv2.rectangle(frame, (xh, yh), (xh + wh, yh + hh), (0, 56, 250), 2)
        cv2.line(frame, (xb, yb + hb - 40), (xb + wb, yb + hb - 40), (0, 0, 255), 4)
        cv2.line(frame, (xb + wb, yb - 40), (xb + wb, yb + hb), (0, 0, 255), 4)

    cv2.imshow('Centroid Tracking', frame)
    fps = time.time() - initial
    if fps > 0:
        fps = int(1/fps)
        #print(fps)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
