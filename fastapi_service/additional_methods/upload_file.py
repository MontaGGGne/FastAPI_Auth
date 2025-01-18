from fastapi import UploadFile, File
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import requests

import os
import io
import json

from files.files_dir import upload_dir
from additional_methods.get_env import *
from s3.s3_conn import boto3_conn


async def upload_json(file: UploadFile, user_s3_id: str, filename: str):
    full_path = f"{CORE_FOLDER}/users/{user_s3_id}/{filename}.json"
    # full_path = os.path.join(upload_dir, 'users', user_s3_id, f"{filename}.json")
    # if not os.path.exists(full_path):
    #     os.makedirs(full_path, exist_ok=True)
    try:
        file_content = await file.read()
        json_data = file_content.decode('utf8').replace("'", '"')
        s3 = boto3_conn()
        print(full_path)
        test = {
            "1": 1,
            "2": 2
        }
        # s3_read.put_object(Bucket='mg-work', Key='fastapi-service/test/test.json', Body=json.dumps(test), StorageClass='COLD')
        # s3.put_object(Bucket='mg-work', Key='fastapi-service/test/test.json', Body=json.dumps(test), ContentType='binary/octet-stream', StorageClass='COLD')
        response = s3.generate_presigned_post( 
            Bucket=BUCKET_ID, 
            Key=full_path , 
            Conditions= None , 
            ExpiresIn= 3600
        )
        print(response)
        fields = response['fields']
        url = response['url']
        put_response = requests.post(response['url'], data=response['fields'],
                             files={'file': json_data})
        print(put_response)
        file.close()
        return full_path
    except Exception as e:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload file go wrong: {repr(e)}"
        )
    finally:
        file.file.close()