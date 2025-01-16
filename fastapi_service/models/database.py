from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from additional_methods.get_env import USER, PASS, HOST, PORT, DBNAME


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