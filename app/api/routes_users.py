from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.dependencies import get_db, get_current_user, get_history_db
from app.models.history import UserHistory
from app.models.user import User
from app.forms.register_form import RegisterForm
from app.forms.login_form import LoginForm
from app.middleware.sessions import get_session_user, set_session_user
from app.middleware.sessions import flash, get_flashed_messages, clear_session_user


from app.services import AuthService
from app.services.history_service import log_event

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
    users = await service.get_all_users(request)
    await service.order_by_id(users)
    errors = form.errors

    if request.method == "POST":
        if not form.is_valid():
            flash(request, "Incorrect field filling.", category="error")
        else:
            result = await service.register(form, request)

            if result:
                flash(request, "Registration successful!", category="success")
            else:
                flash(request, "Registration failed!", category="error")
                return templates.TemplateResponse("welcome.html", {
                    "request": request,
                    "title": "Welcome",
                    "messages": messages
                })

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
        result = await service.login(form, request)
        if result:
            flash(request, "Login successful!", category="success")
            return RedirectResponse(url="/", status_code=303)
        else:
            return templates.TemplateResponse("welcome.html", {
                "request": request,
                "title": "Welcome",
                "messages": messages
            })
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
    user_id = get_current_user(request)
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
async def logout(request: Request, db=Depends(get_db)):
    user = await get_current_user(request)
    clear_session_user(request)
    flash(request, "You have been logged out.", category="success")
    await log_event(user, "Login",
                    f"User: {user.name} successfully logged out")
    return RedirectResponse(url="/", status_code=303)


@users_router.get("/delete_user")
async def delete_user(request: Request, db=Depends(get_db)):
    user = await get_current_user(request)
    user_id = get_session_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Удаляем пользователя из базы
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

    # Очищаем сессию
    clear_session_user(request)
    flash(request, "Your account has been deleted.", category="info")
    await log_event(user, "Login",
                    f"User: {user.name} successfully deleted their account")
    return RedirectResponse(url="/", status_code=303)


@users_router.api_route("/update_user", methods=["GET", "POST"])
async def update(
        request: Request,
        db: AsyncSession = Depends(get_db),
):
    current_user = await get_current_user(request)
    print("User found in route:", current_user.name)
    messages = get_flashed_messages(request)
    service = AuthService(db)

    if not current_user:
        print("В роуте!")
        return RedirectResponse(url="/login", status_code=303)
    print("User found in route:", current_user.email)
    form = RegisterForm(request)
    await form.load_data()
    errors = form.errors

    if request.method == "POST":
        if not form.is_valid():
            flash(request, "Incorrect field filling.", category="error")
        else:
            await service.update_user(form, request)
            try:
                await db.commit()
                flash(request, "Profile updated successfully!", category="success")
                await log_event(current_user, "Update", f"User {current_user.name} updated profile info")
                return RedirectResponse(url="/", status_code=303)
            except Exception as e:
                await db.rollback()
                flash(request, "Error updating profile", category="error")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "form": form,
        "messages": messages,
        "errors": errors,
        "user": current_user,
        "show_modal": True,
        "title": "Update Profile"
    })

@users_router.get("/history")
async def get_history(db: AsyncSession = Depends(get_history_db)):
    result = await db.execute(select(UserHistory))
    entries = result.scalars().all()
    return [
        {
            "timestamp": str(e.timestamp),
            "action": e.action,
            "details": e.details
        } for e in entries
    ]

