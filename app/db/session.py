from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# database url
DATABASE_URL = "sqlite:///./users.db"


# create database engine
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})


# create session local
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)