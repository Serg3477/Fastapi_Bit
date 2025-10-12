from datetime import datetime
from app.models.history import UserHistory
from app.core.db_history import SessionHistory
from app.models.user import User  # для type hinting

async def log_event(user: User, action: str, details: str = ""):
    async with SessionHistory() as session:
        log = UserHistory(
            user_name=user.name,
            timestamp=datetime.utcnow(),
            action=action,
            details=details,

        )
        session.add(log)
        await session.commit()

