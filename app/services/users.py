from sqlalchemy.orm import Session

from app.models.user import UserDB
from app.schemas.user import UserCreate


# create user service
def create_user(db: Session, user_data: UserCreate) -> UserDB:
    user = UserDB(
        name=user_data.name, email=user_data.email, phone_number=user_data.phone_number
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# get all user service
def get_all_users(db: Session) -> list[UserDB]:
    return db.query(UserDB).order_by(UserDB.id).all()


# get user by id service
def get_user_by_id(db: Session, user_id: int) -> UserDB | None:
    return db.get(UserDB, user_id)


# update user service
def update_user(db: Session, user: UserDB, user_data: UserCreate) -> UserDB:
    user.name = user_data.name.strip()
    user.email = user_data.email.strip()
    user.phone_number = user_data.phone_number.strip()

    db.commit()
    db.refresh(user)

    return user


# delete user service
def delete_user(db: Session, user: UserDB) -> None:
    db.delete(user)
    db.commit()
