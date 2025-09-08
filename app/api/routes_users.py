from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_302_FOUND

from app.dependencies import get_db
from app.forms import LoginForm
from app.forms import RegisterForm
from app.forms import AddActiveForm
from app.middleware.sessions import flash
from app.services import ActivesService
from app.middleware import get_flashed_messages


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
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    service = ActivesService(db)
    actives = await service.get_all_actives(request)
    messages = get_flashed_messages(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "actives": actives,
        "messages": messages,
        "title": "Main page of the site"
    })


@router.api_route("/create", methods=["POST", "GET"])
async def create_post(request: Request, db: AsyncSession = Depends(get_db)):
    messages = get_flashed_messages(request)
    form = AddActiveForm(request)
    await form.load_data()
    errors = form.errors
    if request.method == "POST":
        if form.is_valid(request):
            service = ActivesService(db)
            result = await service.create_active(form)

            if not result:
                flash(request, "Error creating active", category="error")
            else:
                flash(request, "Created successfully!", category="success")
            return templates.TemplateResponse("create.html", {
                "request": request,
                "form": form,
                "errors": errors,
                "messages": messages,
            })
    # GET-запрос — просто отображаем пустую форму
    return templates.TemplateResponse("create.html", {
        "request": request,
        "form": form, # или WTForm, если используешь
        "errors": errors,
        "messages": messages
    })

@router.get("/delete/{active_id}")
async def delete_active(active_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    service = ActivesService(db)
    success = await service.delete_active_by_id(active_id)

    if success:
        flash(request, "Record deleted successfully!", category="success")
    else:
        flash(request, "Record not found or could not be deleted", category="error")
    return RedirectResponse("/", status_code=303)


@router.api_route("/update/{active_id}", methods=["POST", "GET"])
async def update(active_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    messages = get_flashed_messages(request)
    form = AddActiveForm(request)
    await form.load_data()
    errors = form.errors
    if request.method == 'POST':

        service = ActivesService(db)
        result = await service.update_active_by_id(form, active_id)
        if not result:
            flash(request, "Error updatingting active", category="error")
        else:
            flash(request, "Updated successfully!", category="success")
        return templates.TemplateResponse("update.html", {
            "request": request,
            "form": form,
            "errors": errors,
            "messages": messages,
        })
        # GET-запрос — просто отображаем пустую форму
    return templates.TemplateResponse("update.html", {
        "request": request,
        "form": form,  # или WTForm, если используешь
        "errors": errors,
        "messages": messages
    })



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
            "errors": "Please fill all fields",
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
            "errors": "Please provide a name and price",
        })
    # логика добавления актива
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)