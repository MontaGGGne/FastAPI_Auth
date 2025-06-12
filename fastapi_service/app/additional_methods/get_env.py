import os
from dotenv import load_dotenv
import logging


dotenv_load_info = load_dotenv()
DOTENV_INFO_1 = dotenv_load_info
DOTENV_INFO_2 = None
print(f"dotenv_load_info 1: {dotenv_load_info}")
logging.info(f"dotenv_load_info 1: {dotenv_load_info}")
cur_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.dirname(os.path.dirname(os.path.dirname(cur_dir)))
if dotenv_load_info is False:
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    core_dir = os.path.dirname(os.path.dirname(os.path.dirname(cur_dir)))
    print(f"Full path: {os.path.join(core_dir, '.env')}")
    logging.info(f"Full path: {os.path.join(core_dir, '.env')}")
    dotenv_load_info = load_dotenv(os.path.join(core_dir, '.env'))
    DOTENV_INFO_2 = dotenv_load_info
    print(f"dotenv_load_info 2: {dotenv_load_info}")
    logging.info(f"dotenv_load_info 2: {dotenv_load_info}")

FULL_PATH = os.path.join(core_dir, '.env')


# DB connection
USER=os.environ.get('DB_USER')
PASS=os.environ.get('DB_PASSWORD')
HOST=os.environ.get('DB_HOST')
PORT=os.environ.get('FASTAPI_DB_PORT')
DBNAME=os.environ.get('FASTAPI_PG_DB')

# S3 connection
AWS_ACCESS_READ_KEY_ID = os.environ.get('AWS_ACCESS_READ_KEY_ID')
AWS_SECRET_ACCESS_READ_KEY = os.environ.get('AWS_SECRET_ACCESS_READ_KEY')
BUCKET_ID = os.environ.get('BUCKET_ID')
CORE_FOLDER = os.environ.get('CORE_FOLDER')
# BUCKET_ID = 'mg-work'
# CORE_FOLDER = 'fastapi-service'