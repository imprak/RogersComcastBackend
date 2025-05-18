from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import User, UserCreate
from app.dependencies.db_session import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Placeholder for user creation logic
    return {"id": 1, "username": user.username}