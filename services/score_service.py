from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.score_model import Score
from models.score_model import Score
from repositories.score_repository import ScoreRepository

class ScoreService:

    def __init__(self):
        self.repository = ScoreRepository()


    def create(self, db: Session, score: Score) -> Response_Model[Score]:
        response: Response_Model = Response_Model(status="success", message="Score created successfully")

        flag: bool = False
        result: Score = None
        try:
            input_score = Score(username = score["username"], score = score["score"])
            self.repository.create(db, input_score, False)
            
            db.commit()
            db.refresh(input_score)
            flag = True
        except: 
            db.rollback()

        
        if flag:
            response.data = result
        else:
            response.status = "error"
            response.message = "Failed to create score"
        
        return response
    

    def update(self, db: Session, session: str) -> Response_Model[Score]:
        response: Response_Model = Response_Model(status="success", message="Score update successful")

        # existing_login = self.repository.find_login_by_session(db, session)
        # if not existing_login:
        #     response.status = "error"
        #     response.message = "Login session does not exist"
        #     return response 

        # result: bool = self.repository.update_score(db, session)
        # if result:
            
        # else:
        #     response.status = "error"
        #     response.message = "Logout failed"

        return response
