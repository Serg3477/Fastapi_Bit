from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.core import settings
from app.core import init_db
from app.api import active_router
from app.api import users_router
# from app.api.routes_admin import router as admin_router
from app.middleware import get_flashed_messages

# 👇 lifespan: замена on_event("startup") Это функция, инициализации базы (например, Base.metadata.create_all),
# подключения к внешним сервисам, выполнения миграций, логирования, и т.д.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    # можно добавить shutdown-логику

app = FastAPI(
    title="FastAPI Altcoins",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(active_router)
app.include_router(users_router)

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/static/Images", StaticFiles(directory="app/static/Images"), name="images")
app.mount("/Avatars", StaticFiles(directory="Avatars"), name="avatars")
templates = Jinja2Templates(directory="app/templates")

# Подключаем middleware для сессий
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Возвращает список сообщений, которые были сохранены через flash().
def template_context_processor(request: Request):
    return {
        "messages": get_flashed_messages(request)
    }

# Добавляет template_context_processor как глобальную переменную в Jinja2.
templates.env.globals["template_context_processor"] = template_context_processor

