from fastapi import UploadFile
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import requests
import traceback

from app.additional_methods.get_env import *
from app.s3.s3_methods import boto3_conn, s3_post_signature


async def upload_json(file: UploadFile, s3_full_path: str):
    try:
        file_content = await file.read()
        json_data = file_content.decode('utf8').replace("'", '"')

        print(f"BUCKET_ID: {BUCKET_ID}")
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
            detail=(f"REPR: {repr(e)}\n",
                    f"DOTENV_INFO_1: {DOTENV_INFO_1}\nDOTENV_INFO_1: {DOTENV_INFO_2}\n",
                    f"FULL_PATH: {FULL_PATH}\nUpload file go wrong: {traceback.format_exc()}")
        )
    finally:
        file.file.close()