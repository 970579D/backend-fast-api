from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.user_model import User
from models.score_model import Score
from repositories.user_repository import UserRepository
from repositories.score_repository import ScoreRepository

class UserService:

    def __init__(self):
        self.repository = UserRepository()
        self.scoreRepository = ScoreRepository();

    def get_all_users(self, db: Session) -> Response_Model[list[User]]:
        return self.repository.get_all_user(db)

    def find_user(self, db: Session, username: str) -> Response_Model[User]:
        return self.repository.find_user(db, username)

    def create(self, db: Session, user: User) -> Response_Model[User]:
        response: Response_Model = Response_Model(status="success", message="Login created successfully")

        existing_user = self.repository.find_user(db, user, isPassword=False)
        if existing_user:
            response.status = "error"
            response.message = "User already exists"
            return response

        flag: bool = False
        result: User = None
        try:
            input_user = User(username = user["username"], password = user["password"])
            # input_score = Score(username=user.username)

            self.repository.create(db, input_user, False)
            # self.scoreRepository.create(db, input_score, False)
            
            db.commit()
            db.refresh(input_user) #add database model, use shortcut
            # db.refresh(input_score)
            # result = self.repository.find_user(db, user, False)
            flag = True
        except: 
            db.rollback()
        

        if flag:
            response.status = "success"
            response.message = "User created successfully"
            response.data = result
        else:
            response.status = "error"
            response.message = "Failed to create user"
        
        return response