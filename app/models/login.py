from sqlalchemy import Column, Integer, String, Boolean
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    psw = Column(String)
    remember = Column(Boolean)
    # submit