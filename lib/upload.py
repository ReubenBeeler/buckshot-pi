import os
import boto3
from typing import Mapping
from mypy_boto3_s3 import S3Client

from lib.require_env import require_env

@require_env('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'AWS_BUCKET')
def upload(*, input_path:str, s3_output_path:str, metadata:Mapping[str, str]|None=None) -> None:
	s3_client: S3Client = boto3.client(
		's3',
		aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
		aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
		region_name=os.getenv('AWS_REGION')
	)

	AWS_BUCKET:str = os.environ['AWS_BUCKET']

	print(f"Pushing to AWS S3 {AWS_BUCKET}")

	with open(input_path, 'rb') as f:
		s3_client.put_object(
			Bucket=AWS_BUCKET,
			Key=s3_output_path,
			Body=f,
			ContentType='image/jpg',
			StorageClass='INTELLIGENT_TIERING',
			Metadata=metadata # pyright: ignore[reportArgumentType]
		)