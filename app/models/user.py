from sqlalchemy import Column, Integer, String
from app.core.db_users import UserBase

class User(UserBase):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    psw = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    db_filename = Column(String, nullable=True)
