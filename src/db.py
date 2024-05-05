import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = (
    f"postgresql://postgres:{os.getenv("POSTGRES_ROOT_PASSWORD")}"
    f"@{os.getenv("POSTGRES_HOST", "localhost")}:"
    f"{os.getenv("POSTGRES_PORT", 5432)}/"
    f"{os.getenv("POSTGRES_DB_NAME", "face-encoding")}"
)

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
