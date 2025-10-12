from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, text
from typing import List
import os
from werkzeug.utils import secure_filename

from app.core import create_user_database, settings
from app.dependencies import get_current_user
from app.middleware.sessions import set_session_user
from app.models import User
from app.middleware import flash
from app.services.history_service import log_event


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db



    async def get_all_users(self, request: Request) -> List[User]:
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        if not users:
            flash(request, "No users records found", category="info")
        users.sort(key=lambda a: a.id)
        return users


    async def login(self, form, request):
        result = await self.db.execute(
            select(User).where(User.name == form.name)
        )
        user = result.scalars().first()
        if not user:
            flash(request, "There is no user registered with this name.", category="error")
            await log_event(user, "Login",
                            f"User: {user.name} trying to login without registration")
            return None

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(form.psw, user.psw):
            set_session_user(request, user.id, remember=form.remember)
            await log_event(user, "Login",
                            f"User: {user.name} successfully logined")
            return user
        else:
            flash(request, "Incorrect password", category="error")
            await log_event(user, "Login",
                            f"User: {user.name} trying to login with incorrect password")
            return None


    async def register(self, form, request: Request) -> bool:
        # Проверка уникальности
        existing = await self.db.execute(
            select(User).where((User.name == form.name) | (User.email == form.email))
        )
        if existing.scalars().first():
            flash(request, "User with this name or email already exists.", category="error")
            return False
        else:
            # Хешируем пароль
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashed_password = pwd_context.hash(form.psw)

            # Обработка аватара
            avatar_path = None
            if form.avatar and getattr(form.avatar, "filename", ""):
                # Пользователь загрузил файл
                orig_name = secure_filename(form.avatar.filename)
                file = f"{form.name}_{orig_name}"
                avatar_path = os.path.join("Avatars", file)
                os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
                with open(avatar_path, "wb") as f:
                    f.write(await form.avatar.read())
            else:
                # Пользователь не выбрал файл → ставим дефолт
                avatar_path = "static/Images/default.png"
            # Создаём пользователя
            user = User(
                name=form.name,
                email=form.email,
                psw=hashed_password,
                avatar=avatar_path,
            )
            try:
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)

                # Создаём индивидуальную БД
                db_filename = f"db_{user.id}.db"
                db_path = os.path.join(settings.USER_DB_DIR, db_filename)
                os.makedirs(settings.USER_DB_DIR, exist_ok=True)
                create_user_database(db_path)

                # Обновляем поле db_filename
                user.db_filename = db_path
                await self.db.commit()

                # Сразу логиним пользователя
                set_session_user(request, user.id, remember=getattr(form, "remember", False))
                await log_event(user, "Register",
                                f"User: {user.name} successfully registered")
                return True
            except Exception as e:
                await self.db.rollback()
                flash(request, "Registration failed due to a database error.", category="error")
                return False


    async def order_by_id(self, users: list):
        # Получаем все записи по возрастанию текущего id
        users = (await self.db.execute(
            select(User).order_by(User.id)
        )).scalars().all()

        # Перенумеровываем
        for new_id, user in enumerate(users, start=1):
            user.id = new_id

        # Сохраняем изменения
        await self.db.commit()

        # Сбрасываем счётчик AUTOINCREMENT в SQLite
        await self.db.execute(text("DELETE FROM sqlite_sequence WHERE name='actives'"))
        await self.db.commit()


    async def update_user(self, form, request: Request) -> bool:
        user = await get_current_user(request)
        # Обновляем поля
        user.name = form.name
        user.email = form.email

        # Обновляем пароль, если введён
        if form.psw:
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            user.psw = pwd_context.hash(form.psw)

        # Обновляем аватар
        if form.avatar and getattr(form.avatar, "filename", ""):
            orig_name = secure_filename(form.avatar.filename)
            file = f"{form.name}_{orig_name}"
            avatar_path = os.path.join("Avatars", file)
            os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
            with open(avatar_path, "wb") as f:
                f.write(await form.avatar.read())
            user.avatar = avatar_path

        await self.db.merge(user)
        return True
