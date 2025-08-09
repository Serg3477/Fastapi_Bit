from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    psw = Column(String)
    remember = Column(Boolean)
    # submit


    # Optional: связи
    # user = relationship("User", backref="results")
    # active = relationship("Active", backref="results")