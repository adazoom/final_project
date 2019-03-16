# Gaze-Detection

Before running code please initiate the server by running:
'python websocket.py'

To run code please run: 
'python main.py'

Our library relies on Python3, Flask, libuvc and pyuvc. 
Please follow the setup instructions listed in the libuvc and pyuvc libraries carefully.

** main.py
This code  already sets up the server and the set up process. 
Please not that the address of the camera might change as it is depending on the driver installed. Therefore, please provide your own data in uvc.Capture()


## Pupil detection using Fast Radio Sysmetric algoirthm are inside matlab folder
## For Webcam support: run the webcam.py in webcam repository