import re

from fastapi import Request

class RegisterForm:
    def __init__(self, request: Request):
        self.request = request
        self.name: str = ""
        self.email: str = ""
        self.psw: str = ""
        self.avatar: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.email = form.get("email")
        self.psw = form.get("psw")
        self.avatar = form.get("avatar")

        self.errors = {}


    def is_valid(self) -> bool:
        # Имя: не пустое, минимум 3 символа
        if not self.name or len(self.name) < 3:
            self.errors["name"] = "Name must be at least 3 characters."

        # Email: базовая проверка формата
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not self.email or not re.match(email_regex, self.email):
            self.errors["email"] = "Invalid email format."

        # Пароль: минимум 6 символов, хотя бы одна цифра и буква
        if not self.psw or len(self.psw) < 6:
            self.errors["psw"] = "Password must be at least 6 characters."
        elif not re.search(r"[A-Za-z]", self.psw) or not re.search(r"\d", self.psw):
            self.errors["psw"] = "Password must contain letters and numbers."

        # Аватар: необязателен, но можно добавить проверку расширения
        if self.avatar and not self.avatar.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            self.errors["avatar"] = "Avatar must be a .png, .jpg, or .jpeg file."

        return not self.errors