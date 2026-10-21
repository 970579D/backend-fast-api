from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, String, DateTime, text
from sqlalchemy.orm import Mapped

from database import Base


class User(Base):
    __tablename__ = "users"

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

    password: Mapped[str] = Column(
        String(255),
        nullable=False,
    )

    create_date: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    last_update: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

class UserRequest(BaseModel):
    username: str
    password: str
