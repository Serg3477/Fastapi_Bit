from fastapi import Request

class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.email: str = ""
        self.psw: str = ""
        self.remember: bool

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.psw = form.get("psw")
        self.remember = form.get("remember") == "on"

    # def is_valid(self) -> bool:
    #     return bool(self.username and self.password)