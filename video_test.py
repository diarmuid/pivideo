__author__ = 'diarmuid'

import picamera

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_recording('my_video.h264.avi',format='h264',profile='baseline')
    camera.wait_recording(10)
    camera.stop_recording()