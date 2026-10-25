from ast import stmt

from sqlalchemy import update
from sqlalchemy.orm import Session

from models.score_model import Score

class ScoreRepository:

    def create(
        self,
        db: Session,
        score: Score,
        is_commit : bool = True
    ) -> bool:
        
        db.add(score)

        if is_commit:
            db.commit()
            db.refresh(score)

        return True

    def update(self, db: Session, score: dict) -> bool:
        result = db.execute(
            update(Score)
            .where(Score.username == score["username"])
            .values(score=score["score"])
        )
        db.commit()
        return result.rowcount > 0