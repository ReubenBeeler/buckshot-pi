#!/usr/bin/env python3
"""
Capture image with PiCamera2
"""

from time import sleep
from picamera2 import Picamera2 # pyright: ignore[reportMissingImports]
import libcamera # pyright: ignore[reportMissingImports]

def capture(output_path: str) -> None:
	picam2 = Picamera2()

	try:
		# Initialize camera
		config = picam2.create_still_configuration()
		config["transform"] = libcamera.Transform(hflip=1, vflip=1) # 180deg rot
		picam2.configure(config)

		# Capture image
		picam2.start()
		sleep(1)
		picam2.capture_file(output_path)
		picam2.stop()
	finally:
		if 'picam2' in locals():
			picam2.close()

# TODO make main for testing