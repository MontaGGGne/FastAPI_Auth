from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import HTTPException

import logging
from boto3.session import Session


logging.basicConfig(level=logging.INFO, filename="py_log_connection.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def boto3_conn(key_id: str, secret_key: str):
    try:
        session = Session()
        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id = key_id,
            aws_secret_access_key = secret_key)
        logging.info("[Connection] Succsessful boto3 connection")
    except Exception as e:
        s3 = None
        logging.error(repr(e))
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="S3 connection error"
        )
    return s3