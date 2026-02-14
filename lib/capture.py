from time import sleep
from picamera2 import Picamera2 # pyright: ignore[reportMissingImports]
import libcamera # pyright: ignore[reportMissingImports]

def capture(output_path: str) -> None:
	"""
	Capture image with PiCamera2
	"""
	try:
		print('Initializing camera...')
		picam2 = Picamera2()
		config = picam2.create_still_configuration()
		config["transform"] = libcamera.Transform(hflip=1, vflip=1) # 180deg rot since my raspi is mounted upside down
		picam2.configure(config)

		print('Capturing image...')
		picam2.start()
		sleep(1) # give the pi time to adjust the exposure and whatnot
		picam2.capture_file(output_path)
		picam2.stop()
	finally:
		if 'picam2' in locals():
			picam2.close()

if __name__ == '__main__':
	import sys
	from argparse import ArgumentParser, Namespace

	parser = ArgumentParser(sys.argv[0], description='Capture an image with picamera2')
	parser.add_argument('output_path', type=str)

	parsed: Namespace = parser.parse_args(sys.argv[1:])

	capture(parsed.output_path)