from pydantic import BaseModel

class ResultBase(BaseModel):
    quantity: int
    price: int

class ResultCreate(ResultBase):
    pass

class ResultRead(ResultBase):
    id: int

    class Config:
        orm_mode = True