import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
from urllib.request import urlopen 


def get_pupil_region(eye_frame):
    kernel = np.ones((3, 3), np.uint8)
    new_frame = cv2.bilateralFilter(eye_frame,10, 15, 15)
    new_frame = cv2.threshold(new_frame, 50, 255, cv2.THRESH_BINARY)[1]
    new_frame = cv2.erode(new_frame, kernel, iterations=3)
    new_frame = cv2.dilate(new_frame, kernel, iterations=2)
    return new_frame


def fit_pupil(frame):
    height, width = frame.shape[:2]
    center = (width / 2, height / 2)
    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)
    try:
        moments = cv2.moments(contours[-2])
        x = int(moments['m10'] / moments['m00'])
        y = int(moments['m01'] / moments['m00'])
    except IndexError:
        pass
    elli = cv2.fitEllipse(contours[-2])
    return x,y,elli
    

def detect_gaze(x, center_x):
    hr = x / (center_x * 2)
    if hr <= left_ratio:
        text = "right"
    elif hr >= right_ratio:
        text = "left"
    else :
        text = "center"
    return text

def processGaze(lastGaze, currentGaze):
    if lastGaze != currentGaze:
        print("turning " + currentGaze)
        urlopen('http://localhost:5000/' + currentGaze);  
    return currentGaze

#  pipeline 
fps = 45
left_ratio = 0.43
right_ratio = 0.6
vidcap = cv2.VideoCapture('./data/eye1.mp4')
succes,image = vidcap.read();
modified = get_pupil_region(image);
modified1 = cv2.cvtColor(modified, cv2.COLOR_BGR2GRAY);
center_x, center_y, _ = fit_pupil(modified1);
frame_height= image.shape[0]
frame_width = image.shape[1]
out = cv2.VideoWriter('out_gaze_detection.avi',cv2.VideoWriter_fourcc('M','J','P','G'), fps, (frame_width,frame_height))

success,image = vidcap.read()
urlopen('http://localhost:5000/refresh');  
count = 0
success = True
lastGaze = 'center'
while success:
    success,image = vidcap.read()
    if success == True:
        # count += 1
        pupil_region = get_pupil_region(image)
        pupil_region_gray = cv2.cvtColor(pupil_region, cv2.COLOR_RGB2GRAY)
        cx, cy, ellipse = fit_pupil(pupil_region_gray)
        gaze_state_text = detect_gaze(cx, center_x)
        lastGaze = processGaze(lastGaze, gaze_state_text)
        cv2.ellipse(image, ellipse,(0,255,0), 1)
        cv2.circle(image, (cx,cy), 3, (0,0,255), thickness=1, lineType=8, shift=0) 
        modified_frame = cv2.putText(image, gaze_state_text, (20, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (147, 58, 31), 2)
        # cv2.imshow('demo', modified_frame)
        out.write(modified_frame)
out.release()

