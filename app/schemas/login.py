from pydantic import BaseModel, EmailStr

class LoginBase(BaseModel):
    email: EmailStr
    psw: str
    remember: bool = False  # по умолчанию не сохраняем сессию на устройстве пользователя

    class Config:
        orm_mode = True