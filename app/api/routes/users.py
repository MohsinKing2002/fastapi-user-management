from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.users import create_user, get_all_users

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/all", response_model=list[UserResponse])
def get_all_users_endpoint(db: Session = Depends(get_db)) -> list[UserResponse]:
    return get_all_users(db)

@router.post("/new", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    try:
        user = create_user(db, user_data)
        return user
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc