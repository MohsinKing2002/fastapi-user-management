from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)

# api router
router = APIRouter(prefix="/users", tags=["Users"])


# all users endpoint
@router.get("/all", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users_endpoint(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_all_users(db)


# get user by id endpoint
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(
    user_id: int, db: Session = Depends(get_db)
) -> UserResponse:
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


# new user creation endpoint
@router.post("/new", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_data: UserCreate, db: Session = Depends(get_db)
) -> UserResponse:
    try:
        user = create_user(db, user_data)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        ) from exc


# update user endpoint
@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(
    user_id: int, user_data: UserCreate, db: Session = Depends(get_db)
) -> UserResponse:
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    try:
        return update_user(db, user, user_data)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email may already exist.",
        ) from exc


# delete user endpoint
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)) -> None:
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    delete_user(db, user)
