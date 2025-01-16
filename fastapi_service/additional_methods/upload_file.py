from fastapi import UploadFile, File
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import os
import shutil

from files.files_dir import upload_dir


def upload_json(file, user_s3_id: str, filename: str):
    try:
        full_path = f"{upload_dir}/users/{user_s3_id}/{filename}.json"
        with open(full_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        return full_path
    except Exception:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Upload file go wrong'
        )
    finally:
        file.file.close()