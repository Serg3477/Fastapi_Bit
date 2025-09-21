from fastapi import APIRouter, Request, Depends, UploadFile, Form
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from app.core.db import get_db
from app.models.user import User
from app.forms.register_form import RegisterForm
from passlib.hash import bcrypt
from app.middleware.sessions import flash, get_flashed_messages
from app.core.templates import templates
import os

router = APIRouter()

@router.api_route("/register", methods=["GET", "POST"])
async def register(request: Request, db=Depends(get_db)):
    form = RegisterForm(request)
    await form.load_data()
    messages = get_flashed_messages(request)

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
                    avatar_path = os.path.join("Images", filename)
                    with open(avatar_path, "wb") as f:
                        f.write(await form.avatar.read())

                # Создаём пользователя
                user = User(
                    name=form.name,
                    email=form.email,
                    hashed_password=hashed_password,
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
