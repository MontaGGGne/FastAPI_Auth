import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import URL
from dotenv import load_dotenv


load_dotenv()

pg_connect_url = URL.create(
    "postgresql+psycopg2",
    username=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('FASTAPI_DB_PORT'),
    database=os.environ.get('FASTAPI_PG_DB'),
)

engine = create_engine(
    pg_connect_url
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()