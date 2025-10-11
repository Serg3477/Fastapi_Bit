from sqlalchemy import Column, Integer, String, Float
from datetime import date
from app.core.db_tenant import TenantBase

class Actives(TenantBase):
    __tablename__ = "actives"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, default=date.today)
    token = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)



