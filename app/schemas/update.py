from wsgiref.validate import validator

from pydantic import BaseModel

class ActiveUBase(BaseModel):
    token: str
    quantity: float
    price: float
    amount: float

class ActiveUpdate(ActiveUBase):
    id: int

    @validator("token", "quantity", "price", "amount")
    def positive_value(cls, token, quantity, price, amount):
        if len(token) < 3:
            raise ValueError("Token must be at least 3 characters long")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return token, quantity, price, amount

    class Config:
        orm_mode = True
