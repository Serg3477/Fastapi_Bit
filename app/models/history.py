from sqlalchemy import Column, Integer, String, DateTime
from app.core.db_history import HistoryBase


class UserHistory(HistoryBase):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    timestamp = Column(DateTime)
    action = Column(String)
    details = Column(String)


