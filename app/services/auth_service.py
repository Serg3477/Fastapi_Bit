from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, text
from typing import List
import os
from werkzeug.utils import secure_filename

from app.middleware.sessions import set_session_user
from app.models import User
from app.middleware import flash


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_actives(self, request: Request) -> List[User]:
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        if not users:
            flash(request, "No users records found", category="info")
        users.sort(key=lambda a: a.id)
        return users


    async def login(self, form, request):
        result = await self.db.execute(
            select(User).where((User.name == form.name))
        )
        user = result.scalars().first()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if user and pwd_context.verify(form.psw, user.psw):  # или check_password_hash
            set_session_user(request, user.id, remember=form.remember)
            return user


    async def register(self, form, request: Request) -> bool:
        # Проверка уникальности
        existing = await self.db.execute(
            select(User).where((User.name == form.name) | (User.email == form.email))
        )
        if existing.scalars().first():
            flash(request, "User with this name or email already exists.", category="error")
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
                avatar=avatar_path
            )
            try:
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)

                # ✅ Сразу логиним пользователя
                set_session_user(request, user.id, remember=getattr(form, "remember", False))

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
