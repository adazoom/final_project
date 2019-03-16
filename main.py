#!/usr/bin/env python3
from __future__ import print_function
import multiprocessing
import queue
from urllib.request import urlopen

import cv2
import pyuvc.uvc as uvc

from pupil1 import PupilDetector
from websocket import webserver


def main():
    # Create the shared queue
    event_queue = multiprocessing.Queue()

    # Start the webserver
    web_process = multiprocessing.Process(target=webserver, kwargs={
        'event_queue': event_queue,
    })
    web_process.start()

    try:
        camera_process(event_queue)
    except:
        print('Camera process failed (fragile)')
        raise
    finally:
        print("Killing Webserver")
        web_process.terminate()


def camera_process(event_queue):
    # Grab the camera
    dev_list = uvc.device_list()
    print(dev_list)
    #cap = uvc.Capture(dev_list[0]["uid"])
    cap = uvc.Capture("20:29")

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

        # Check if there are any updates from our webserver
        try:
            event = event_queue.get_nowait()
        except queue.Empty:
            pass
        else:
            # Handle event
            if event['id'] == 'recenter':
                print('CENTER')
                pupil_detector.recenter(frame)
                continue
            elif event['id'] == 'align_left':
                print('LEFT')
                pupil_detector.align_left(frame)
            elif event['id'] == 'align_right':
                print('RIGHT')
                pupil_detector.align_right(frame)

            # This frame is a bust, we've used it already
            continue

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

        # Show the debug image (For initial camera alignment)
        cv2.imshow(
            'demo',
            pupil_detector.debug_frame()
        )
        cv2.waitKey(1)


if __name__ == '__main__':
    main()

