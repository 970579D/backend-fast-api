from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.score_model import Score
from models.score_model import Score
from repositories.score_repository import ScoreRepository

class ScoreService:

    def __init__(self):
        self.repository = ScoreRepository()


    def create(self, db: Session, score: Score) -> Response_Model[Score]:
        response: Response_Model = Response_Model(status="success", message="Login created successfully")

        flag: bool = False
        result: Score = None
        try:
            print("log")
            print(score)
            input_score = Score(username = score["username"], score = score["score"])

            self.repository.create(db, input_score, False)
            
            db.commit()
            db.refresh(input_score) #add database model, use shortcut
            flag = True
        except: 
            db.rollback()

        
        if flag:
            response.status = "success"
            response.message = "Score created successfully"
            response.data = result
        else:
            response.status = "error"
            response.message = "Failed to create score"
        
        return response
    
    