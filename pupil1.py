import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

# .5 is the middle
# LEFT_RATIO = 0.55
# RIGHT_RATIO = 0.46
LEFT_RATIO = 0.06
RIGHT_RATIO = 0.05

class PupilDetector(object):

    def recenter(self, frame):
        self.center_x, self.center_y = self.fit_pupil(frame)      
    
    def detect_gaze(self, frame):
        x, _ = self.fit_pupil(frame)
        if x is None:
            return 'blink'

        hr = x / (self.center_x * 2)
        if hr <= (.5 - RIGHT_RATIO):
            text = "right"
        elif hr >= (.5 + LEFT_RATIO):
            text = "left"
        else :
            text = "center"

        self.gaze_state_text = text

        return text

    def fit_pupil(self, frame):
        pupil_region = get_pupil_region(frame.gray)
        # pupil_region = cv2.cvtColor(pupil_region, cv2.COLOR_RGB2GRAY)

        height, width = pupil_region.shape[:2]
        center = (width / 2, height / 2)
        contours, _ = cv2.findContours(pupil_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=cv2.contourArea)

        try:
            if len(contours) == 1:
                return None, None
                #eye_contour = contours[0]
            elif len(contours) == 0:
                return None, None
            else:
                eye_contour = contours[-2]

            moments = cv2.moments(eye_contour)
            x = int(moments['m10'] / moments['m00'])
            y = int(moments['m01'] / moments['m00'])
        except IndexError:
            pass

        self.eye_contour = eye_contour
        self.weird_frame = pupil_region
        self.real_frame = frame.bgr

        return x, y

    def debug_frame(self):
        # frame = self.weird_frame
        frame = self.real_frame #this is the normal frame

        ellipse = cv2.fitEllipse(self.eye_contour)

        cv2.ellipse(frame, ellipse, (0,255,0), 1)
        cv2.circle(frame, (self.center_x, self.center_y), 3, (0,0,255), thickness=1, lineType=8, shift=0) 
        modified_frame = cv2.putText(frame, self.gaze_state_text, (20, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (147, 58, 31), 2)

        return modified_frame


def get_pupil_region(eye_frame):
    kernel = np.ones((3, 3), np.uint8)
    new_frame = cv2.bilateralFilter(eye_frame,10, 15, 15)
    new_frame = cv2.threshold(new_frame, 50, 255, cv2.THRESH_BINARY)[1]
    new_frame = cv2.erode(new_frame, kernel, iterations=3)
    new_frame = cv2.dilate(new_frame, kernel, iterations=2)
    return new_frame
    

# def processGaze(lastGaze, currentGaze):
#     if lastGaze != currentGaze:
#         print("turning " + currentGaze)
#         urlopen('http://localhost:5000/' + currentGaze)

# def pupil_detect(frame):
#     pupil_region = get_pupil_region(frame)
#     pupil_region_gray = cv2.cvtColor(pupil_region, cv2.COLOR_RGB2GRAY)
#     cx, cy, ellipse = fit_pupil(pupil_region_gray)
#     gaze_state_text = detect_gaze(cx, center_x)
#     return gaze_state_text

if __name__ == '__main__':
    #  pipeline 
    fps = 45
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
            


            # cv2.imshow('demo', modified_frame)
            out.write(modified_frame)
    out.release()

