from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.score_model import Score
from models.score_model import Score
from repositories.score_repository import ScoreRepository
from utils import constants, utils

class ScoreService:

    def __init__(self):
        self.repository = ScoreRepository()

    def create(self, db: Session, score: Score) -> Response_Model[Score]:
        res: Response_Model = Response_Model(status="success", message=utils.res_status_msg(constants.SCORE, constants.SUCCESS))

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
            res.data = result
        else:
            res.status = constants.ERROR
            res.message = utils.res_status_msg(constants.Logout, constants.ERROR)
        
        return res
    

    def update(self, db: Session, score: dict) -> Response_Model[Score]:
        res: Response_Model = Response_Model(status="success", message=utils.res_status_msg(constants.SCORE, constants.SUCCESS))

        result: bool = self.repository.update(db, score)
        if result == False:
            res.status = constants.ERROR
            res.message = utils.res_status_msg(constants.Logout, constants.ERROR)

        return res
