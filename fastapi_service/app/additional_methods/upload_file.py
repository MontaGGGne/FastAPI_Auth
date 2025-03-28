from fastapi import UploadFile
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import requests

from app.additional_methods.get_env import *
from app.s3.s3_methods import boto3_conn, s3_post_signature


async def upload_json(file: UploadFile, s3_full_path: str):
    try:
        file_content = await file.read()
        json_data = file_content.decode('utf8').replace("'", '"')

        response = s3_post_signature(s3_session=boto3_conn(),
                                     bucket=BUCKET_ID,
                                     key=s3_full_path)

        put_response = requests.post(response['url'],
                                     data=response['fields'],
                                     files={'file': json_data})
        file.file.close()
        if put_response.reason != 'No Content':
            raise HTTPException(
                status_code=put_response.status_code,
                detail=f"Post to s3 error"
            )
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload file go wrong: {repr(e)}"
        )
    finally:
        file.file.close()