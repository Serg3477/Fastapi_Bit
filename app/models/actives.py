from sqlalchemy import Column, Integer, String, Float
from app.core.db import Base

class Actives(Base):
    __tablename__ = "actives"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    quantity = Column(Float, unique=True, nullable=False)
    price = Column(Float, unique=True, nullable=False)
    amount = Column(Float, unique=True, nullable=False)
    # submit = SubmitField('Save')

    category = Column(String)

