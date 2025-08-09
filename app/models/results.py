from sqlalchemy import Column, Integer, String, Float
import datetime
from app.core.db import Base

class Actives(Base):
    __tablename__ = "actives"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, default=datetime.datetime.utcnow)
    token = Column(String, unique=True, nullable=False)
    quantity = Column(Float, unique=True, nullable=False)
    price = Column(Float, unique=True, nullable=False)
    profit = Column(Float, unique=True, nullable=False)