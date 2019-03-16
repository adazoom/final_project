#  evaluate 

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

def get_pupil_region(eye_frame):
    kernel = np.ones((3, 3), np.uint8)
    new_frame = cv2.bilateralFilter(eye_frame,10, 15, 15)
    new_frame = cv2.threshold(new_frame, 55, 255, cv2.THRESH_BINARY)[1]
    new_frame = cv2.erode(new_frame, kernel, iterations=3)
    new_frame = cv2.dilate(new_frame, kernel, iterations=3)
    return new_frame

def fit_pupil(frame):
    _, contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)
    try:
        moments = cv2.moments(contours[-2])
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])
    except IndexError:
        pass
    elli = cv2.fitEllipse(contours[-2])
    return cx, cy, elli
    
v = cv2.VideoCapture('./1.avi')
ground_truth_file = open("./1.txt","r") 
succes,image = v.read()
plt.imshow(image)
gt = []
for line in ground_truth_file:
    l = str.split(line)
    x = float(l[0])
    y = float(l[1])
    gt.append((x,y))

success = True
count = 0
MSE = 0
print(len(gt))
precise_count = 0
precise_mse = 0
unprecise_mse = 0
while success:
    if(count == 1000):
        break
    success,image = v.read()
    pupil_region = get_pupil_region(image);
    pupil_region_gray = cv2.cvtColor(pupil_region, cv2.COLOR_RGB2GRAY);
    cx, cy, ellipse = fit_pupil(pupil_region_gray);
    gt_xy = gt[count]
    cv2.circle(image, (cx,cy), 3, (0,255,255), thickness=1, lineType=8, shift=0) 
    cv2.circle(image, (int(gt_xy[0]), int(gt_xy[1])), 3, (255,0,255), thickness=1, lineType=8, shift=0) 
    mse = (cx - gt_xy[0]) * (cx - gt_xy[0]) + (cy - gt_xy[1]) * (cy - gt_xy[1])
    if mse < 25.0:
        precise_mse = precise_mse + mse
        precise_count = precise_count + 1
    else:
        unprecise_mse = unprecise_mse + mse
    MSE = MSE + mse
    count = count + 1
    plt.imshow(image)

MSE = MSE/count
print('mse is %f'% MSE)
print('precise mse is %f'% float(precise_mse/precise_count))
print('precise percentage is %f'% float(precise_count/count))
