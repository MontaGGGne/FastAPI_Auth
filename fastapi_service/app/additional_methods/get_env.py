import os
from dotenv import load_dotenv


load_dotenv()

# DB connection
USER=os.environ.get('DB_USER')
PASS=os.environ.get('DB_PASSWORD')
HOST=os.environ.get('DB_HOST')
PORT=os.environ.get('FASTAPI_DB_PORT')
DBNAME=os.environ.get('FASTAPI_PG_DB')

# S3 connection
AWS_ACCESS_READ_KEY_ID = os.environ.get('AWS_ACCESS_READ_KEY_ID')
AWS_SECRET_ACCESS_READ_KEY = os.environ.get('AWS_SECRET_ACCESS_READ_KEY')
BUCKET_ID = 'mg-work'
CORE_FOLDER = 'fastapi-service'