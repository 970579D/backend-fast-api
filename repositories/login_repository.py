from ast import stmt

from sqlalchemy import func, select, update
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
        result: Login = list(
            db.scalars(select(Login).where(Login.username == username).where(Login.logout_date.is_(None)))
        )
        return result

    def find_login_by_session(self, db: Session, session: str) -> Login:
        result: Login = list(
            db.scalars(select(Login).where(Login.session == session).where(Login.logout_date.is_(None)))
        )
        return result

    def create_login(
        self,
        db: Session,
        login: Login,
    ) -> Login:
        input_login = Login(username=login.username, session=login.session)
        db.add(input_login)
        db.commit()
        db.refresh(input_login)
        selected_login = self.find_login(db, login.username)
        return selected_login

    def logout(self, db: Session, session: str) -> bool:
        result = db.execute(
            update(Login)
            .where(Login.session == session)
            .where(Login.logout_date.is_(None))
            .values(logout_date=func.now())
        )
        db.commit()
        return result.rowcount > 0