# Gaze-Detection

- Implementation of the working page turning system:
  Before running code please initiate the server by running:
  'python websocket.py'

  To run code please run: 
  'python main.py'

  To open the page turning system please open the 
  'index.html' in Page turning software folder

  Our library relies on Python3, Flask, libuvc and pyuvc and dlib. 
  Please follow the setup instructions listed in the libuvc and pyuvc libraries carefully.

  ** main.py
  This code  already sets up the server and the set up process. 
  Please not that the address of the camera might change as it is depending on the driver installed. Therefore, please provide your own data in uvc.Capture()

- Pupil detection using Fast Radio Sysmetric algoirthm is in matlab folder, please run 
'pupil_detection.m' in matlab

- For Webcam support, please run 
'python webcam.py' in webcam repository
