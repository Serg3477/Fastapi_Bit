from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    psw = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
