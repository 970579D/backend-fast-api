from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.user_model import User
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.repository = UserRepository()

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

        result: User = self.repository.create(db, user)

        if result:
            response.status = "success"
            response.message = "User created successfully"
            response.data = result
        else:
            response.status = "error"
            response.message = "Failed to create user"
        
        return response