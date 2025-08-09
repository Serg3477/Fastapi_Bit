from pydantic import BaseModel, EmailStr

class RegisterBase(BaseModel):
    email: EmailStr
    psw: str
    remember: bool = False  # по умолчанию не сохраняем сессию на устройстве пользователя

class UserCreate(RegisterBase):
    psw: str  # вводит чистый пароль

class UserRead(RegisterBase):
    id: int

    class Config:
        orm_mode = True