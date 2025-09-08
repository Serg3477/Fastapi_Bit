from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash

from app.models import User



class AuthService:
    async def login(request, db: AsyncSession, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not check_password_hash(user.psw, password):
            return False, "Invalid email or password", None
        return True, "Welcome!", user

auth_service = AuthService()