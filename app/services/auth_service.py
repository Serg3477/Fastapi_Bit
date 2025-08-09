from models import User
from core.db import db
from werkzeug.security import check_password_hash

class AuthService:
    async def login(self, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        if not user or not check_password_hash(user.psw, password):
            return False, "Invalid email or password", None
        return True, "Welcome!", user

auth_service = AuthService()