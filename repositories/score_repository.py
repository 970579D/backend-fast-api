from ast import stmt

from sqlalchemy import desc, select, update
from sqlalchemy.orm import Session

from models.score_model import Score

class ScoreRepository:
       
    def find_last_round(self, db: Session, username: str) -> Score:
        result = db.scalars(
        select(Score)
        .where(Score.username == username)
        .order_by(desc(Score.round))
        .limit(1)
    ).first()
        
        return result
    
    def create(
        self,
        db: Session,
        score: Score
    ) -> bool:
        
        db.add(score)
        db.commit()
        db.refresh(score)

        return True

    def update(self, db: Session, score: Score) -> bool:
        result = db.execute(
            update(Score)
            .where(Score.username == score["username"])
            .values(score=score["score"])
        )
        db.commit()
        return result.rowcount > 0