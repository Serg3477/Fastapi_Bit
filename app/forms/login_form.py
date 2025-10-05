from fastapi import Request

class LoginForm:
    def __init__(self, request: Request):
        self.request = request
        self.name: str = ""
        self.psw: str = ""
        self.remember: bool
        self.errors: list[str] = []

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.psw = form.get("psw")
        self.remember = form.get("remember") == "on"

    def is_valid(self) -> bool:
        self.errors = {}

        if not self.name:
            self.errors["name"] = "Username or email is required."

        if not self.psw:
            self.errors["psw"] = "Password is required."

        return not self.errors
