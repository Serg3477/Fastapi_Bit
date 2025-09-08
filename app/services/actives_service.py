from fastapi import Request, Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.forms import AddActiveForm
from app.middleware import flash
from app.models import Actives
from typing import List
from datetime import datetime


class ActivesService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_all_actives(self, request: Request) -> List[Actives]:
        result = await self.db.execute(select(Actives))
        actives = result.scalars().all()
        if not actives:
            flash(request, "No active records found", category="info")
        actives.sort(key=lambda a: a.id)
        return actives


    async def create_active(self, form_data) -> bool:
        token = form_data.token
        quantity = float(form_data.quantity)
        price = float(form_data.price)
        amount = price * quantity
        data = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        existing = await self.db.execute(
            select(Actives).where(Actives.token == token)
        )
        rec = existing.scalar_one_or_none()

        if rec:
            active = await self.buying_same_token(rec, quantity, price, amount)
        else:
            active = Actives(data=data, token=token, quantity=quantity, price=price, amount=amount)

        try:
            self.db.add(active)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            print(f"Error saving active: {e}")
            return False

    @staticmethod
    async def buying_same_token(self, rec: Actives, quantity: float, price: float, amount: float) -> Actives:
        sum_quantity = rec.quantity + quantity
        average_price = ((rec.quantity * rec.price) + (quantity * price)) / sum_quantity
        sum_amount = rec.amount + amount

        rec.quantity = sum_quantity
        rec.price = round(average_price, 2)
        rec.amount = sum_amount

        print('Average price:', average_price)
        return rec

    async def delete_active_by_id(self, active_id: int) -> bool:
        try:
            result = await self.db.execute(
                delete(Actives).where(Actives.id == active_id)
            )
            if result.rowcount == 0:
                return False  # ничего не удалено
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting active: {e}")
            return False

    async def update_active(self, active_id: int, form_data) -> bool:
        try:
            result = await self.db.execute(
                select(Actives).where(Actives.id == active_id)
            )
            active = result.scalar_one_or_none()
            if not active:
                return False  # актив не найден
            active.token = form_data.token
            active.quantity = float(form_data.quantity)
            active.price = float(form_data.price)
            active.amount = active.quantity * active.price
            self.db.add(active)
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            print(f"Error updating active: {e}")
            return False

