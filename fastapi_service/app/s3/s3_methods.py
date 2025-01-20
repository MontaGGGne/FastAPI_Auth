from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import HTTPException

import logging
from boto3.session import Session, Config

from app.additional_methods.get_env import *


logging.basicConfig(level=logging.INFO, filename="py_log_connection.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def boto3_conn():
    try:
        session = Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id = AWS_ACCESS_READ_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_READ_KEY,
            region_name='us-east-1',
            config=Config(signature_version='s3v4')
        )
        logging.info("[Connection] Succsessful boto3 connection")
    except Exception as e:
        s3 = None
        logging.error(repr(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="S3 connection error"
        )
    return s3

def s3_post_signature(s3_session, bucket, key):
    return s3_session.generate_presigned_post( 
        Bucket=bucket, 
        Key=key, 
        Conditions=None, 
        ExpiresIn=3600
    )

def s3_get_signature(s3_session, bucket, key):
    return s3_session.generate_presigned_url(
        "get_object",
        Params={
                "Bucket": bucket,
                "Key": key
            },
        ExpiresIn=3600
    )