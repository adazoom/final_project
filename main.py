#!/usr/bin/env python3
from __future__ import print_function
import pyuvc.uvc as uvc
import logging
import cv2
from urllib.request import urlopen 
from pupil1 import PupilDetector

logging.basicConfig(level=logging.INFO)


FPS = 45


# print(cap.avaible_modes)
def main():
    # Grab the camera
    dev_list = uvc.device_list()
    print(dev_list)
    cap = uvc.Capture(dev_list[0]["uid"])
    # cap = uvc.Capture("20:10")

    # controls_dict = dict([(c.display_name, c) for c in cap.controls])
    # controls_dict['Auto Exposure Mode'].value = 1
    # controls_dict['Gamma'].value = 200

    urlopen('http://localhost:5000/refresh')

    initial_frame = cap.get_frame_robust()

    # Pupil Detection
    pupil_detector = PupilDetector()
    pupil_detector.recenter(initial_frame)

    lastGaze = 'center'
    has_blinked = False
    while True:
        frame = cap.get_frame_robust()

        currentGaze = pupil_detector.detect_gaze(frame)
        if currentGaze == 'blink':
            if has_blinked:
                pass
            else:
                print("turning " + lastGaze)
                urlopen('http://localhost:5000/' + lastGaze)
                has_blinked = True
        else:
            lastGaze = currentGaze
            has_blinked = False

        cv2.imshow('demo', 
            pupil_detector.debug_frame()
        )
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

