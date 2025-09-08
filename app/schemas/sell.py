from wsgiref.validate import validator

from pydantic import BaseModel

class ActiveSBase(BaseModel):
    quantity: float
    price: float


class ActiveSell(ActiveSBase):
    id: int

    @validator("quantity", "price")
    def positive_value(cls, quantity, price):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        return quantity, price

    class Config:
        orm_mode = True

