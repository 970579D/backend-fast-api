from sqlalchemy import select
from sqlalchemy.orm import Session

from models.response_model import Response_Model
from models.user_model import User

class UserRepository:

    def get_all_user(self, db: Session) -> Response_Model[list[User]]:
       users: list[User] = list(
                   db.scalars(select(User)).all()
               )
       return Response_Model(status="success", message="Users found", data=users
    )

    def find_user(self, db: Session, user: User, isPassword: bool) -> User:
        user: User | None = db.scalars(select(User).where(
        User.username == user["username"],
        User.password == user["password"]
    ) if isPassword else
    select(User).where(
        User.username == user["username"]
    )).one_or_none()
        
        return user

    def create(
        self,
        db: Session,
        user: User,
    ) -> bool:
        
        db.add(user)
        db.commit()
        db.refresh(user)

        return True
    