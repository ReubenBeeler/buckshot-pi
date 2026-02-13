#!/usr/bin/env python

from picamera2 import Picamera2
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()
result = picam2.capture_file("test.jpg")
import pdb; pdb.set_trace()
picam2.close()
