from sqlalchemy import create_engine
from app.core.db_tenant import TenantBase

def create_user_database(db_path: str):
    engine = create_engine(f"sqlite:///{db_path}")
    TenantBase.metadata.create_all(engine)




