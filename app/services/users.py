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


def get_all_users(db: Session) -> list[UserDB]:
    return db.query(UserDB).order_by(UserDB.id).all()