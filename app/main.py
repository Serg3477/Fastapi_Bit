from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from starlette.middleware.sessions import SessionMiddleware

from app.core.init_db import init_db
from app.api.routes_users import router as users_router
from app.api.routes_admin import router as admin_router
from app.middleware.sessions import get_flashed_messages

# 👇 lifespan: замена on_event("startup")
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
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.add_middleware(SessionMiddleware, secret_key="sga34er8a04tg348[gng8n")

def template_context_processor(request: Request):
    return {
        "messages": get_flashed_messages(request)
    }

templates.env.globals["template_context_processor"] = template_context_processor