from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/stile"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Class for a db session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Class inherited from by models
Base = declarative_base()
