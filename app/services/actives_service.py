from fastapi import Request
from sqlalchemy import select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.middleware import flash
from app.models import Actives
from app.models import Results
from typing import List
from datetime import datetime, date


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


    async def get_all_results(self, request: Request) -> List[Actives]:
        result = await self.db.execute(select(Results))
        results = result.scalars().all()
        if not results:
            flash(request, "No active records found", category="info")
        results.sort(key=lambda a: a.id)
        return results


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
            active = self.buying_same_token(rec, quantity, price, amount)
        else:
            active = Actives(data=data, token=token, quantity=quantity, price=price, amount=amount)

        try:
            self.db.add(active)
            await self.db.commit()
            await self.db.refresh(active)
            return True
        except Exception as e:
            await self.db.rollback()
            return False

    @staticmethod
    def buying_same_token(rec: Actives, quantity: float, price: float, amount: float) -> Actives:
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


    async def delete_result_by_id(self, result_id: int) -> bool:
        try:
            result = await self.db.execute(
                delete(Results).where(Results.id == result_id)
            )
            if result.rowcount == 0:
                return False  # ничего не удалено
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            print(f"Error deleting result: {e}")
            return False


    async def update_active(self, active_id: int, form_data):
        try:
            active = await self.db.get(Actives, active_id)
            if not active:
                return None

            # Обновляем только непустые поля
            for field in ["token", "quantity", "price", "data"]:
                value = getattr(form_data, field, None)
                if value not in (None, ""):
                    if field in ("quantity", "price"):
                        value = float(value)
                    setattr(active, field, value)
            active.amount = active.quantity * active.price

            await self.db.commit()
            await self.db.refresh(active)
            return active

        except Exception as e:
            await self.db.rollback()
            print(f"Error updating active: {e}")
            return None


    async def order_by_id(self, actives: list):
        # Получаем все записи по возрастанию текущего id
        actives = (await self.db.execute(
            select(Actives).order_by(Actives.id)
        )).scalars().all()

        # Перенумеровываем
        for new_id, active in enumerate(actives, start=1):
            active.id = new_id

        # Сохраняем изменения
        await self.db.commit()

        # Сбрасываем счётчик AUTOINCREMENT в SQLite
        await self.db.execute(text("DELETE FROM sqlite_sequence WHERE name='actives'"))
        await self.db.commit()


    async def order_by_id_rec(self, records: list):
        # Получаем все записи по возрастанию текущего id
        records = (await self.db.execute(
            select(Results).order_by(Results.id)
        )).scalars().all()

        # Перенумеровываем
        for new_id, record in enumerate(records, start=1):
            record.id = new_id

        # Сохраняем изменения
        await self.db.commit()

        # Сбрасываем счётчик AUTOINCREMENT в SQLite
        await self.db.execute(text("DELETE FROM sqlite_sequence WHERE name='results'"))
        await self.db.commit()


    async def sell_active(self, active_id, rec, form):
        if rec:
            act_date_buy = rec.data
            act_date_sell = str(date.today())
            act_date = f"{act_date_buy}  -  {act_date_sell}"
            if form.is_valid():
                token = rec.token
                quantity = form.quantity
                price = form.price
                profit = (float(form.quantity) * float(form.price)) - (
                            float(form.quantity) * float(rec.price))
                results = Results(data=act_date, token=token, quantity=quantity, price=price, profit=profit)
                try:
                    self.db.add(results)
                    await self.db.commit()
                    # logger.info(f'Active {token} were sold with profit {profit}.')
                    await self.delete_active_by_id(active_id)
                    dat = float(form.quantity)
                    if dat < rec.quantity:  # Если продавать меньше общей суммы токенов(не все)
                        rec.quantity = rec.quantity - float(form.quantity)
                        rec.amount = rec.amount - (float(form.quantity) * float(rec.price))
                        actives = Actives(data=rec.data, token=token, quantity=rec.quantity, price=rec.price,
                                          amount=rec.amount)
                        self.db.add(actives)
                        await self.db.commit()
                    return results
                except Exception as e:
                    print(f"Error during creating record: {e}")
