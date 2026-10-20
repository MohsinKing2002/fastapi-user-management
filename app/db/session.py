from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
db_url = settings.database_url

# connection arguments
connection_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

# create database engine
engine = create_engine(db_url, connect_args=connection_args)


# create session local
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
