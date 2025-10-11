from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db_history import HistoryBase


class UserHistory(HistoryBase):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(String)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="logs")
