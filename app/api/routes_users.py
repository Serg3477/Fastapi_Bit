from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND

from app.forms.login_form import LoginForm
from app.forms.register_form import RegisterForm
from app.forms.add_active_form import AddActiveForm
from app.middleware.sessions import flash
from app.services.actives_service import ActivesService
from app.services.actives_service import actives_service
from app.middleware.sessions import get_flashed_messages


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

menu = [
    {"name": "Main page", "url": "/"},
    {"name": "Create new record", "url": "/create"},
    {"name": "Show profits", "url": "/main"},
    {"name": "Authorization", "url": "/login"},
    {"name": "Profile", "url": "/profile"},
    {"name": "Admin panel", "url": "/admin/login"}
]



@router.get("/")
async def index(request: Request):
    actives = actives_service.get_all_actives()
    messages = get_flashed_messages(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "actives": actives,
        "messages": messages,
        "title": "Main page of the site"
    })


@router.post("/create")
async def create_post(request: Request, form_data: dict = Depends(...)):
    result = await ActivesService.create_active(form_data)
    if not result:
        flash(request, "Error creating active", category="error")
    else:
        flash(request, "Created successfully", category="success")
    return RedirectResponse("/", status_code=302)




@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(request: Request):
    form = RegisterForm(request)
    await form.load_data()
    if not form.is_valid():
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Please fill all fields",
        })
    # логика сохранения пользователя
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)


@router.get("/add-active", response_class=HTMLResponse)
async def add_active_form(request: Request):
    return templates.TemplateResponse("add_active.html", {"request": request})

@router.post("/add-active")
async def add_active(request: Request):
    form = AddActiveForm(request)
    await form.load_data()
    if not form.is_valid():
        return templates.TemplateResponse("add_active.html", {
            "request": request,
            "error": "Please provide a name and price",
        })
    # логика добавления актива
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)