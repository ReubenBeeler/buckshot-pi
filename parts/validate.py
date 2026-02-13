#!/usr/bin/env python3
"""
Validate image using AWS Lambda function
"""

import os
import json
from typing import Any
import boto3
import base64
from mypy_boto3_lambda import LambdaClient

from parts.require_env import require_env
from py_util.collections import Optional, chain

# def is_type(d, *args, _type:type) -> bool:
# 	assert isinstance(_type, type), '_type must be of type `type`'
# 	c = chain(d, *args)
# 	if c is None: return False
# 	return isinstance(c.get(), _type)

@require_env('AWS_LAMBDA_FUNCTION_NAME', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION')
def validate(input_path: str|None, test:bool = False) -> Optional[dict[str, Any]]:
	try:
		payload:dict
		if test:
			assert input_path is None
			payload = {"test": True}
		else:
			assert input_path is not None

			print('Reading image buffer...')

			with open(input_path, 'rb') as input_buffer:
				image_bytes: bytes = input_buffer.read()
			
			image_bytes_b64: bytes = base64.b64encode(image_bytes)
			image_b64: str = image_bytes_b64.decode('utf-8')
			payload = {'image': image_b64}

		lambda_client: LambdaClient = boto3.client(
			'lambda',
			aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
			aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
			region_name=os.getenv('AWS_REGION')
		)
		
		function_name:str = os.environ['AWS_LAMBDA_FUNCTION_NAME']

		print(f'Invoking AWS Lambda function...')
		response = lambda_client.invoke(
			FunctionName=function_name,
			Payload=json.dumps(payload)
		)

		payload = json.loads(response['Payload'].read().decode('utf-8'))

		# Make a json deserializable type for payload?
		if 'statusCode' in payload and payload['statusCode'] == 200:
			valid:bool = payload['valid']
			return Optional(payload['prediction']) if valid else Optional()
		else:
			sts:str|None = payload.get('stackTraceString', None)
			if isinstance(sts, str):
				print(f"Lambda Stack Trace:\n\t{sts.replace('\n', '\t\n')}")
			raise Exception('Lambda function failed!', payload)
	except Exception as e:
		print(f"Error: {e}")
		raise

# TODO make main for testing