__author__ = 'diarmuid'

# raspivid -n -w 960 -h 720 -b 3300000 -t 0 -fps 30 -g 90 -pf high -ih -o - |
#  avconv -r 30 -i -  -vcodec copy -f mpegts  udp://235.0.0.1:8010?pkt_size=1316

import socket
import time
import picamera
import subprocess,io,os
import time


class ConversionOutput(object):
    def __init__(self, camera):
        print('Spawning background conversion process')
        self.converter = subprocess.Popen([
            'avconv',
            '-i', '-',
            '-fflags','igndts',
            '-vcodec','copy',
            '-f', 'mpegts',
            '-mpegts_original_network_id', '0x1122',
            '-mpegts_transport_stream_id', '0x3344',
            '-mpegts_service_id', '0x5566',
            '-mpegts_pmt_start_pid', '0x1500',
            '-mpegts_start_pid', '0x150',
            '-metadata','service_provider="Diarmuids Channel"',
            '-metadata', 'service_name="RaspberryLive"',
            'udp://192.168.1.39:8010?pkt_size=1316'],
            stdin=subprocess.PIPE,stderr=io.open(os.devnull, 'wb'),stdout=subprocess.PIPE,
            shell=False, close_fds=True)

    def write(self, b):
        #print "Here"
        self.converter.stdin.write(b)

    def flush(self):
        print('Waiting for background conversion process to exit')
        self.converter.stdin.close()
        self.converter.wait()




with picamera.PiCamera() as camera:
    camera.resolution = (1296, 972)
    camera.framerate = 30

    # Accept a single connection and make a file-like object out of it
    connection = ConversionOutput(camera)
    #try:
    camera.start_recording(connection, format='h264',profile='high')
    try:
        while True:
            camera.wait_recording(0.1)
            camera.annotate_text = "{}".format(time.strftime("%H:%M:%S", time.gmtime()))
    finally:
        camera.stop_recording()

    #camera.stop_recording()
    #finally:
        #connection.close()
        #connection.flush()