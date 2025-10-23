from fastapi import Request, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import SessionUsers
from app.models import User


def get_session_user(request: Request) -> int | None:
    user_id = request.session.get("user_id")
    print("→ session user_id:", user_id)
    return user_id


# чтобы сохранить его ID в сессии и optionally включить "запомнить меня"
def set_session_user(request: Request, user_id: int, remember: bool = False):
    request.session["user_id"] = user_id
    if remember:
        # Устанавливаем флаг, можно использовать для расширенного хранения
        request.session["remember"] = True


async def login_required(request: Request = Depends()):
    user_id = get_session_user(request)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    return user_id


def clear_session_user(request: Request):
    request.session.pop("user_id", None)
    request.session.pop("remember", None)

# Возвращает список сообщений, которые были сохранены через flash().
def template_context_processor(request: Request):
    return {
        "messages": get_flashed_messages(request)
    }


#  Сохраняет flash-сообщение в сессии, сообщение сохраняется в cookie
# category — может быть "info", "success", "error" и т.д. Используется для CSS-классов.
def flash(request: Request, message: str, category: str = "info"):
    if "_flashes" not in request.session:
        request.session["_flashes"] = []
    request.session["_flashes"].append((category, message))


# чтобы узнать, авторизован ли пользователь
def get_flashed_messages(request: Request) -> list[tuple[str, str]]:
    # удаляет список сообщений из сессии и возвращает его. Если сообщений нет, возвращает пустой список
    return request.session.pop("_flashes", [])





