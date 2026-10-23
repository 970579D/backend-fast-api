from ast import stmt

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from models.score_model import Score
from models.response_model import Response_Model
from models.user_model import User

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
        # selected_score = self.find_score(db, score.username)
        # return selected_score

    def update_score(self, db: Session, session: str) -> bool:
        result = db.execute(
            update(Score)
            .where(Score.session == session)
            .where(Score.logout_date.is_(None))
            .values(logout_date=func.now())
        )
        db.commit()
        return result.rowcount > 0