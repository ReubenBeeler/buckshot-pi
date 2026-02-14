if __name__ == '__main__':
	from dotenv import load_dotenv
	load_dotenv(override=True)

	from require_env import require_env
else:
	from .require_env import require_env

import os
import json
import boto3
from mypy_boto3_lambda import LambdaClient

def split(s: str) -> list[str]:
	return [e.strip() for e in s.split(', ')]

env_var_names: list[str] = split('''
	AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_LAMBDA_FUNCTION_NAME
	''')

@require_env(*env_var_names)
def validate() -> dict:
	"""
	Run image validation with AWS Lambda function
	"""

	AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_LAMBDA_FUNCTION_NAME \
		= (os.environ[name] for name in env_var_names)

	lambda_client: LambdaClient = boto3.client('lambda', region_name=AWS_REGION)
	
	function_name:str = os.environ['AWS_LAMBDA_FUNCTION_NAME']

	print(f'Invoking AWS Lambda function...')
	response = lambda_client.invoke(FunctionName=function_name)

	return json.loads(response['Payload'].read().decode('utf-8'))

if __name__ == "__main__":
	print(json.dumps(validate(), indent=4))