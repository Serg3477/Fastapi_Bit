from fastapi import Request

class AddResultsForm:
    def __init__(self, request: Request):
        self.request = request
        self.quantity: float = 0.0
        self.price: float = 0.0

    async def load_data(self):
        form = await self.request.form()
        self.quantity = float(form.get("quantity") or 0)
        self.price = float(form.get("price") or 0)
