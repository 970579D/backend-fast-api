import uuid

from sqlalchemy.orm import Session

from models.login_model import Login
from models.response_model import Response_Model
from models.user_model import User, UserRequest
from repositories.login_repository import LoginRepository
from repositories.user_repository import UserRepository
import utils.constants as constants
import utils.utils as utils

class LoginService:

    def __init__(self):
        self.repository = LoginRepository()
        self.user_repository = UserRepository()

    def get_all_users(self, db: Session) -> Response_Model[list[User]]:
        response: Response_Model = Response_Model(status=constants.SUCCESS, message=utils.res_status_msg(constants.LOGIN, constants.SUCCESS))
        response["data"] = self.repository.get_all_user(db)
        return response

    def find_login(self, db: Session, username: str) -> Response_Model[Login]:
        response: Response_Model = Response_Model(status=constants.SUCCESS, message=utils.res_status_msg(constants.LOGIN, constants.SUCCESS))
        login = self.repository.find_login(db, username)
        response.data = login
        return response

    def create_login(self, db: Session, login_request: UserRequest) -> Response_Model[Login]:
        response: Response_Model = Response_Model(status=constants.SUCCESS, message=utils.res_status_msg(constants.LOGIN, constants.SUCCESS))

        user = self.user_repository.find_user(db, login_request, isPassword=True)
        print(user)
        if not user:
            response.status = constants.ERROR
            response.message = utils.res_status_msg(constants.LOGIN, constants.ERROR, "Users does not exist or password not match")
            return response
        existing_login = self.repository.find_login(db, login_request["username"])
        if existing_login:
            response.status = constants.ERROR
            response.message = utils.res_status_msg(constants.LOGIN, constants.ERROR, "Login already exists")
            return response

        login_data: Login = Login(
            username=login_request["username"],
            session=self.generate_session_id()
        )

        result: User = self.repository.create_login(db, login_data)
        if result:
            response.data = result
        return response 


    def logout(self, db: Session, session: str) -> Response_Model[Login]:
        response: Response_Model = Response_Model(status=constants.SUCCESS, 
                                                  message=utils.res_status_msg(constants.Logout, constants.SUCCESS))

        existing_login = self.repository.find_login_by_session(db, session)
        if not existing_login:
            response.status = constants.ERROR
            response.message =  utils.res_status_msg(constants.Logout, constants.ERROR, "Login session does not exist")
            return response 

        result: bool = self.repository.logout(db, session)
        if result == False:
            response.status = constants.ERROR
            response.message = utils.res_status_msg(constants.Logout, constants.ERROR)

        return response

    def generate_session_id(self) -> str:
        return str(uuid.uuid4())