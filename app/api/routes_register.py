from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND
from services.auth_service import auth_service
from middleware.sessions import flash
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login")
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_post(request: Request, email: str = Form(...), psw: str = Form(...)):
    success, message, user = await auth_service.login(email, psw)
    if not success:
        flash(request, message, category="error")
        return RedirectResponse("/login", status_code=HTTP_302_FOUND)

    request.session["user_id"] = user.id
    flash(request, "Login successful!", category="success")
    return RedirectResponse("/profile", status_code=HTTP_302_FOUND)
