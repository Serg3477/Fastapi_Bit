from sqlalchemy import Column, Integer, String, Float
from datetime import date
from app.core.db_tenant import TenantBase

class Results(TenantBase):
    __tablename__ = "results"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, default=date.today)
    token = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    profit = Column(Float,nullable=False)
