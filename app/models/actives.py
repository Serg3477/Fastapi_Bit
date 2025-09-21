from sqlalchemy import Column, Integer, String, Float
import datetime
from app.core.db import Base

class Actives(Base):
    __tablename__ = "actives"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, default=datetime.date.today())
    token = Column(String, unique=True, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    # submit = SubmitField('Save')


