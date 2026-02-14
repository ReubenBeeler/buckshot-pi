if __name__ == '__main__':
	from dotenv import load_dotenv
	load_dotenv(override=True) # before other imports so that the environment is setup before the @requires_env decorator runs

import os
import tempfile
from datetime import datetime

from lib import *
from py_util.collections import Optional

def make_copyback_dir() -> str:
	require_env('BUCKSHOT_PROJECT_DIR')
	project_dir:str = os.environ['BUCKSHOT_PROJECT_DIR']
	copyback_path:str = os.path.join(project_dir, '.copyback')
	os.makedirs(copyback_path, exist_ok=True)
	return copyback_path

@require_env('UNVALIDATED_IMAGE_PATH')
def main(*, copy_back:bool=False, capture_only:bool=False) -> None:
	"""
	Capture image with PiCamera2, validate with SpeciesNet inference on AWS Lambda, and upload image to S3
	"""

	UNVALIDATED_IMAGE_PATH:str = os.environ['UNVALIDATED_IMAGE_PATH']

	if copy_back:
		copyback_path:str = make_copyback_dir() # do now for env var check

	timestamp:str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
	
	 # TODO use logging framework (and emojis!)

	with tempfile.NamedTemporaryFile(mode='w+b', delete=True, suffix=".jpg") as tmp_file:
		print(f"Capturing image to {tmp_file.name}...")
		capture(tmp_file.name)

		if copy_back:
			copy_path:str = f'{copyback_path}/{timestamp}.jpg'
			print(f'Copying image to {copy_path}...')
			import shutil
			shutil.copy2(tmp_file.name, copy_path)
		
		if capture_only:
			return
		
		print(f"Uploading to S3...")
		upload(
			input_path=tmp_file.name,
			s3_output_path=f"{UNVALIDATED_IMAGE_PATH}{timestamp}.jpg"
		)

if __name__ == "__main__":
	import sys
	from argparse import ArgumentParser, Namespace

	parser = ArgumentParser(sys.argv[0])
	parser.add_subparsers(title='debug')
	parser.add_argument('--copy-back', action='store_true')
	parser.add_argument('--capture-only', action='store_true')
	pargs: Namespace = parser.parse_args(sys.argv[1:])

	main(copy_back=pargs.copy_back, capture_only=pargs.capture_only)