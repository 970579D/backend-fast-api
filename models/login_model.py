from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, String, DateTime, text
from sqlalchemy.orm import Mapped

from database import Base
#id username login_date logout_date 

class Login(Base):
    __tablename__ = "login"

    id: Mapped[int] = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = Column(
        String(50),
        nullable=False,
        unique=True,
    )
    
    login_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    logout_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=text("CURRENT_TIMESTAMP"),
    )

