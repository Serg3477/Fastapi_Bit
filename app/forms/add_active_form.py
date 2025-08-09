from fastapi import Request

class AddActiveForm:
    def __init__(self, request: Request):
        self.request = request
        self.token: str = ""
        self.quantity: float = 0.0
        self.price: float = 0.0
        self.amount: float = 0.0

    async def load_data(self):
        form = await self.request.form()
        self.token = form.get("token")
        self.quantity = float(form.get("quantity") or 0)
        self.price = float(form.get("price") or 0)
        self.amount = float(form.get("amount") or 0)

    # def is_valid(self) -> bool:
    #     return bool(self.name and self.price > 0)