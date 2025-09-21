from fastapi import Request

from app.middleware import flash


class AddActiveForm:
    def __init__(self, request: Request):
        self.request = request
        self.token: str = ""
        self.quantity: float = 0.0
        self.price: float = 0.0
        self.amount: float = 0.0
        self.errors: list[str] = []

    async def load_data(self):
        form = await self.request.form()
        self.token = form.get("token")
        self.quantity = float(form.get("quantity") or 0)
        self.price = float(form.get("price") or 0)
        self.amount = float(form.get("amount") or 0)

    def is_valid(self, request: Request):
        self.errors = {}
        if not self.token:
            self.errors["token"] = "Token is required"
        if self.quantity <= 0:
            self.errors["quantity"] = "Quantity must be greater than 0"
        if self.price <= 0:
            self.errors["price"] = "Price must be greater than 0"
        return len (self.errors) == 0
