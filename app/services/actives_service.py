from app.models.actives import Actives
from database import db
from typing import List


class ActivesService:
    async def create_active(self, form_data: dict):
        token = form_data["token"]
        ...
        active = Actives(...)
        try:
            db.session.add(active)
            db.session.commit()
            return True
        except Exception as e:
            return False

    def get_all_actives(self) -> List[Actives]:
        actives = db.session.query(Actives).all()
        actives.sort(key=lambda a: a.id)  # альтернатива operations.order_by_id
        return actives

actives_service = ActivesService()