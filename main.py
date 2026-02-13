# TODO make shebang for uv?

from dotenv import load_dotenv
load_dotenv() # before other imports so that the environment is setup before the @requires_env decorator runs

from argparse import Namespace
import os
import tempfile
from datetime import datetime

from lib import *
from py_util.collections import Optional

# TODO make this upload to S3 bucket regardless of validation and then run a separate cronjob for validation at the end of the day for batching
def main(*, debug:bool=False) -> None:
	"""
	Capture image with PiCamera2, validate with SpeciesNet inference on AWS Lambda, and upload image to S3
	"""

	timestamp:str = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
	
	 # TODO use logging framework (and emojis!)

	with tempfile.NamedTemporaryFile(mode='w+b', delete=True, suffix=".jpg") as tmp_file:
		print(f"Capturing image to {tmp_file.name}...")
		capture(tmp_file.name)

		if debug:
			import shutil
			if os.path.isdir('copyback'):
				shutil.copy2(tmp_file.name, 'copyback/output.jpg')
			else:
				print(f'Skipped copying to ./copyback since no ./copyback directory exists. Is debug mode intentional?')
		
		try:
			print(f"Starting validation...")
			validation: Optional[dict[str, Any]] = validate(tmp_file.name)
		except:
			unvalidated_path: str = f"unvalidated/{timestamp}.jpg"
			print(f'Error occurred during validation! Saving image to S3 at {unvalidated_path} for future validation...')
			upload(
				input_path=tmp_file.name,
				s3_output_path=unvalidated_path
			)
			raise
		if validation.has():
			if debug:
				print(f'Image contains wildfile!')
				print(f'Metadata:\n\t{json.dumps(validation.get(), indent=4).replace("\n", "\n\t")}')
			print(f'Beginning upload to S3...')
			upload(
				input_path=tmp_file.name,
				s3_output_path=f"validated/{timestamp}.jpg",
				metadata={k: str(v) for k, v in validation.get().items()}
			)
		else:
			if debug:
				print(f'Image does not contain wildlife. Skipping upload...')


if __name__ == "__main__":
	import sys
	import argparse

	parser = argparse.ArgumentParser(sys.argv[0])
	parser.add_argument('--debug', action='store_true')
	pargs: Namespace = parser.parse_args(sys.argv[1:])

	main(debug=pargs.debug)