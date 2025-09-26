from fastapi import APIRouter, Request, Depends, UploadFile, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.dependencies import get_db
from app.models.user import User
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm
from app.middleware.sessions import get_session_user, set_session_user
from passlib.hash import bcrypt
from app.middleware.sessions import flash, get_flashed_messages, clear_session_user
import os

users_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

menu = [
    {"name": "Main page", "url": "/"},
    {"name": "Create new record", "url": "/create"},
    {"name": "Show profits", "url": "/main"},
    {"name": "Authorization", "url": "/login"},
    {"name": "Profile", "url": "/profile"},
    {"name": "Admin panel", "url": "/admin/login"}
]


@users_router.api_route("/register", methods=["GET", "POST"])
async def register(request: Request, db: AsyncSession = Depends(get_db)):
    form = RegisterForm(request)
    await form.load_data()
    messages = get_flashed_messages(request)
    errors = form.errors

    if request.method == "POST":
        if not form.is_valid():
            flash(request, "Incorrect field filling.", category="error")
        else:
            # Проверка уникальности
            existing = await db.execute(
                select(User).where((User.name == form.name) | (User.email == form.email))
            )
            if existing.scalars().first():
                flash(request, "User with this name or email already exists.", category="error")
            else:
                # Хешируем пароль
                hashed_password = bcrypt.hash(form.psw)

                # Обработка аватара
                avatar_path = None
                if form.avatar:
                    filename = f"{form.name}_{form.avatar.filename}"
                    avatar_path = os.path.join("Avatars", filename)
                    os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
                    with open(avatar_path, "wb") as f:
                        f.write(await form.avatar.read())

                # Создаём пользователя
                user = User(
                    name=form.name,
                    email=form.email,
                    psw=hashed_password,
                    avatar=avatar_path
                )
                db.add(user)
                await db.commit()
                flash(request, "Registration successful!", category="success")
                return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("register.html", {
        "request": request,
        "form": form,
        "messages": messages,
        "title": "Registration"
    })



@users_router.api_route("/login", methods=["GET", "POST"])
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    # Если уже авторизован — перенаправляем
    current_user = get_session_user(request)
    if current_user:
        return RedirectResponse(url="/profile", status_code=303)

    form = LoginForm(request)
    await form.load_data()
    messages = get_flashed_messages(request)

    if request.method == "POST":
        if not form.is_valid():
            for field, msg in form.errors.items():
                flash(request, f"{field}: {msg}", category="error")
        else:
            # Ищем пользователя по имени или email
            result = await db.execute(
                select(User).where(User.name == form.name)
            )
            user = result.scalars().first()

            if user and bcrypt.verify(form.psw, user.psw):
                # Устанавливаем сессию
                set_session_user(request, user.id, remember=form.remember)
                flash(request, "Login successful!", category="success")

                # Перенаправление на next или профиль
                next_url = request.query_params.get("next") or "/profile"
                return RedirectResponse(url=next_url, status_code=303)
            else:
                flash(request, "Incorrect username/email or password.", category="error")

    return templates.TemplateResponse("login.html", {
        "request": request,
        "form": form,
        "messages": messages,
        "title": "Login page"
    })


@users_router.get("/profile")
async def profile(request: Request, db=Depends(get_db)):
    messages = get_flashed_messages(request)
    user_id = get_session_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    flash(request, f"Welcome!", category="success")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "title": "Your Profile"
    })


@users_router.get("/logout")
async def logout(request: Request):
    clear_session_user(request)
    flash(request, "You have been logged out.", category="info")
    return RedirectResponse(url="/login", status_code=303)


@users_router.get("/delete_user")
async def delete_user(request: Request, db=Depends(get_db)):
    user_id = get_session_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Удаляем пользователя из базы
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    # Очищаем сессию
    clear_session_user(request)
    flash(request, "Your account has been deleted.", category="info")

    return RedirectResponse(url="/login", status_code=303)
