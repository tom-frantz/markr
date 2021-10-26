import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:postgres@{POSTGRES_HOST}/stile"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Class for a db session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Class inherited from by models
Base = declarative_base()
