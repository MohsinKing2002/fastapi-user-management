from sqlalchemy.orm import Session

from app.models.user import UserDB
from app.schemas.user import UserCreate

def create_user(db: Session, user_data: UserCreate) -> UserDB:
    user = UserDB(
        name=user_data.name,
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user