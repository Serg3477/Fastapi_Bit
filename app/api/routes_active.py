from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.forms import AddActiveForm
from app.forms import SellActiveForm
from app.middleware.sessions import get_session_user, flash, get_flashed_messages
from app.models import Actives
from app.models import Results
from app.services import ActivesService



active_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

menu = [
    {"name": "Main page", "url": "/"},
    {"name": "Create new record", "url": "/create"},
    {"name": "Show profits", "url": "/main"},
    {"name": "Authorization", "url": "/login"},
    {"name": "Profile", "url": "/profile"},
    {"name": "Admin panel", "url": "/admin/login"}
]



@active_router.get("/")
async def index(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = get_session_user(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    service = ActivesService(db)
    actives = await service.get_all_actives(request)
    await service.order_by_id(actives)
    messages = get_flashed_messages(request)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "actives": actives,
        "messages": messages,
        "title": "Main page of the site"
    })


@active_router.api_route("/create", methods=["POST", "GET"])
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
        "form": form,
        "errors": errors,
        "messages": messages
    })

@active_router.get("/delete/{active_id}")
async def delete_active(active_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    service = ActivesService(db)
    actives = await service.get_all_actives(request)
    success = await service.delete_active_by_id(active_id)
    await service.order_by_id(actives)
    if success:
        flash(request, "Record deleted successfully!", category="success")
    else:
        flash(request, "Record not found or could not be deleted", category="error")
    return RedirectResponse("/", status_code=303)


@active_router.get("/delRec/{result_id}")
async def delete_result(result_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    service = ActivesService(db)
    results = await service.get_all_results(request)
    success = await service.delete_result_by_id(result_id)
    await service.order_by_id_rec(results)
    if success:
        flash(request, "Record deleted successfully!", category="success")
    else:
        flash(request, "Record not found or could not be deleted", category="error")
    return RedirectResponse("/", status_code=303)


@active_router.api_route("/update/{active_id}", methods=["GET", "POST"])
async def update(active_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    messages = get_flashed_messages(request)

    # Загружаем запись один раз
    result = await db.execute(select(Actives).where(Actives.id == active_id))
    active = result.scalars().first()

    if not active:
        flash(request, f"Active with id={active_id} not found", category="error")
        return RedirectResponse(url="/", status_code=303)

    form = AddActiveForm(request)
    await form.load_data()
    errors = form.errors

    if request.method == "POST" and not errors:
        service = ActivesService(db)
        updated = await service.update_active(active_id, form)
        if updated:
            flash(request, "Updated successfully!", category="success")
        else:
            flash(request, "Error updating active", category="error")

    # Передаём в шаблон словарь, чтобы избежать lazy-load
    active_dict = {
        "id": active.id,
        "token": active.token,
        "quantity": active.quantity,
        "price": active.price,
        "amount": active.amount
    }
    return templates.TemplateResponse(
        "update.html",
        {
            "request": request,
            "form": form,
            "errors": errors,
            "messages": messages,
            "active": active_dict
        }
    )


@active_router.get("/main")
async def base(request: Request, db: AsyncSession = Depends(get_db)):
    messages = get_flashed_messages(request)
    service = ActivesService(db)

    # Получаем сумму всех profits
    res1 = await db.execute(select(func.sum(Results.profit)))
    total_sum = res1.scalar() or 0

    # Получаем все записи из Results
    res2 = await db.execute(select(Results).order_by(Results.id))
    results = res2.scalars().all()
    await service.order_by_id(results)
    return templates.TemplateResponse(
        'main.html',
        {
            "request": request,
            "title": 'Database of transaction history',
            "records": results,
            "total_profit": total_sum,
            "messages": messages
        }
    )


@active_router.api_route("/main/{active_id}", methods=['POST', 'GET'])
async def sell(active_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    rec = (await db.execute(select(Actives).where(Actives.id == active_id))).scalars().first()
    messages = get_flashed_messages(request)
    form = SellActiveForm(request)
    await form.load_data()
    errors = form.errors
    results_dict = {
        "id": rec.id,
        "data": rec.data,
        "token": rec.token,
        "quantity": rec.quantity,
        "price": rec.price,
        "amount": rec.amount
    }
    if request.method == "POST" and not errors:
        print ('Method POST')
        service = ActivesService(db)
        updated = await service.sell_active(active_id, rec, form)
        if updated:
            flash(request, "Recording results successfully!", category="success")
            # Обновляем данные для отображения
            # results_dict = {
            #     "id": updated.id,
            #     "date": updated.data,
            #     "token": updated.token,
            #     "quant": updated.quantity,
            #     "price": updated.price,
            #     "amount": updated.amount
            # }
        else:
            flash(request, "Error recording results", category="error")
            # Передаём в шаблон словарь, чтобы избежать lazy-load
    return templates.TemplateResponse(
        "record.html",
        {
            "request": request,
            "form": form,
            "errors": errors,
            "messages": messages,
            "active": results_dict,
            "title": 'Recent token'
        }
    )




