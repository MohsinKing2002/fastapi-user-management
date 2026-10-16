from app.db.base import Base
from app.db.session import engine
from app.models.user import UserDB # -> Registers the model with Base.metadata


# create database tables
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)