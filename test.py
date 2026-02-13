#!/usr/bin/env python

# from picamera2 import Picamera2
# from pprint import pprint
# import pdb

# picam2 = Picamera2()
# camera_config = picam2.create_still_configuration()
# pprint(picam2.camera_controls)
# pprint(dir(picam2.camera_controls))
# pdb.set_trace()

try:
    raise Exception("debug")
except BaseException as e:
    print(f"caught: {e}")
    raise
finally:
    print("finally")
