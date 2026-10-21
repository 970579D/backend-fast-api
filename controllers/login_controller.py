from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.login_service import LoginService

router = APIRouter(prefix="/login", tags=["Login"])

login_service = LoginService()

@router.get("/")
def get_all_logins(db: Session = Depends(get_db)):
    return login_service.get_all_logins(db)

@router.get("/{username}")
def find_login(username: str, db: Session = Depends(get_db)):
    return login_service.find_login(db, username)

@router.post("/")
def create(user: dict, db: Session = Depends(get_db)):
    return login_service.create_login(db, user)