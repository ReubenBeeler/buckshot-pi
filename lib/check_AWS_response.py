
def check_AWS_response(response:dict, err_msg:str) -> None:
	status_code:int = response['ResponseMetadata']['HTTPStatusCode']
	if status_code // 100 != 2:
		raise Exception(f'ERROR: AWS responded with HTTPStatusCode {status_code}: {err_msg}')