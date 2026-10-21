from sqlalchemy import select
from sqlalchemy.orm import Session

from models.login_model import Login
from models.response_model import Response_Model
from models.user_model import User

class LoginRepository:

    #wrap Response_Model at service layer
    def get_all_logins(self, db: Session) -> list[Login]:
       logins: list[Login] = list(
                   db.scalars(select(Login)).all()
               )
       return logins

    def find_login(self, db: Session, username: str) -> Login:
        # logout is null
        login: Login = list(
            db.scalars(select(Login).where(Login.username == username).where(Login.logout_date.is_(None)))
        )
        return login

    def create_login(
        self,
        db: Session,
        login: Login,
    ) -> Login:
        input_login = Login(username=login.username)
        db.add(input_login)
        db.commit()
        db.refresh(input_login)
        selected_login = self.find_login(db, login.username)
        return selected_login
    