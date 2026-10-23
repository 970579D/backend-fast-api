from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services.score_service import ScoreService

router = APIRouter(prefix="/score", tags=["Score"])

score_service = ScoreService()

@router.post("/")
def create(score: dict, db: Session = Depends(get_db)):
    return score_service.create(db, score)

@router.put("/logout")
def logout(session: str, db: Session = Depends(get_db)):
    return score_service.update(db, session)