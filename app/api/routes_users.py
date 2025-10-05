from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.dependencies import get_db
from app.models.user import User
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm
from app.middleware.sessions import get_session_user, set_session_user
from app.middleware.sessions import flash, get_flashed_messages, clear_session_user


from app.services import AuthService

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
    messages = get_flashed_messages(request)
    service = AuthService(db)
    form = RegisterForm(request)
    await form.load_data()
    users = service.get_all_actives(request)
    await service.order_by_id(users)
    errors = form.errors

    if request.method == "POST":
        if not form.is_valid():
            flash(request, "Incorrect field filling.", category="error")
        else:
            result = await service.register(form, request)

            if result:
                flash(request, "Registration successful!", category="success")
                return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "form": form,
        "messages": messages,
        "errors": form.errors
    })




@users_router.api_route("/login", methods=["GET", "POST"])
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    messages = get_flashed_messages(request)
    service = AuthService(db)
    form = LoginForm(request)
    await form.load_data()
    errors = form.errors

    if request.method == "POST":
        if not form.is_valid():
            for field, msg in form.errors.items():
                flash(request, f"{field}: {msg}", category="error")
        else:
            result = await service.login(form, request)
            if result:
                flash(request, "Login successful!", category="success")
                return RedirectResponse(url="/", status_code=303)
            else:
                flash(request, "Incorrect username/email or password.", category="error")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "form": form,
        "messages": messages,
        "errors": form.errors,
        "show_modal": True,
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
    flash(request, "You have been logged out.", category="success")
    return RedirectResponse(url="/", status_code=303)


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

    return RedirectResponse(url="/", status_code=303)
