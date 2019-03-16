import numpy as np
import cv2
import dlib
from scipy.spatial import distance as dist
from pupil1 import PupilDetector
import matplotlib.pyplot as plt
from __future__ import print_function
import logging
import cv2
from urllib.request import urlopen 
logging.basicConfig(level=logging.INFO)

PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat⁩".encode('ascii', errors='ignore')
predictor = dlib.shape_predictor(PREDICTOR_PATH)
detector = dlib.get_frontal_face_detector()
RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))
lastGaze = 'center'
has_blinked = False
pupil_detector = PupilDetector()
left_ratio = 0.45
right_ratio = 0.55

EYE_AR_THRESH = 0.25
EYE_Count = 3

def crop_eye_region(eye, points):
    margin = 2
    min_x = np.min(points[:, 0]) - margin
    max_x = np.max(points[:, 0]) + margin
    min_y = np.min(points[:, 1]) - margin
    max_y = np.max(points[:, 1]) + margin
    origin = (min_x, min_y)
    return eye[min_y:max_y, min_x:max_x,:], origin


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Start capturing the WebCam

video_capture = cv2.VideoCapture(0)
while True:
    ret, frame = video_capture.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        landmarks = predictor(frame, faces[0])
        left_eye_region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in LEFT_EYE_POINTS]).astype(np.int32)
        left_eye_frame, _ = crop_eye_region(frame, left_eye_region)
#         plt.imshow(left_eye_frame)
        
        right_eye_region = np.array([(landmarks.part(point).x, landmarks.part(point).y) for point in RIGHT_EYE_POINTS]).astype(np.int32)
        right_eye_frame, _ = crop_eye_region(frame, right_eye_region)
        plt.imshow(left_eye_frame)

        pupil_detector.geocenter(left_eye_frame)
        currentGaze = pupil_detector.detect_gaze(left_eye_frame)
        print(currentGaze)
        
        
        ear_left = eye_aspect_ratio(left_eye_region)
        ear_right = eye_aspect_ratio(right_eye_region)

        cv2.putText(frame, "E.A.R. Left : {:.2f}".format(ear_left), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, "E.A.R. Right: {:.2f}".format(ear_right), (300, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, currentGaze, (500, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 255), 2)
        
        if ear_left < EYE_AR_THRESH:
            count
            gaze_state = 'blink'
        
        if gaze_state == 'blink':
            if has_blinked:
                pass
            else:
                print("turning " + lastGaze)
                urlopen('http://localhost:5000/' + lastGaze)
                has_blinked = True
        else:
            lastGaze = currentGaze
            has_blinked = False

