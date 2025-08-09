from pydantic import BaseModel

class ActiveBase(BaseModel):
    token: str
    quantity: float
    price: float
    amount: float

class ActiveCreate(ActiveBase):
    pass

class ActiveRead(ActiveBase):
    id: int

    class Config:
        orm_mode = True