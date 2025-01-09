import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()
USER=os.environ.get('DB_USER')
PASS=os.environ.get('DB_PASSWORD')
HOST=os.environ.get('DB_HOST')
PORT=os.environ.get('FASTAPI_DB_PORT')
DBNAME=os.environ.get('FASTAPI_PG_DB')


pg_connect_url = f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}"

engine = create_engine(
    pg_connect_url
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()