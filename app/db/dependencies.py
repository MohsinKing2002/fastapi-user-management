from collections.abc import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal


# database session dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()