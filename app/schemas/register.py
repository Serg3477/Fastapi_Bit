from pydantic import BaseModel, EmailStr

class RegisterBase(BaseModel):
    name: str
    email: EmailStr
    psw: str


class UserCreate(RegisterBase):
    id: int

    class Config:
        orm_mode = True