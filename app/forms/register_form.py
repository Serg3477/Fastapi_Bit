from fastapi import Request

class RegisterForm:
    def __init__(self, request: Request):
        self.request = request
        self.name: str = ""
        self.email: str = ""
        self.psw: str = ""

    async def load_data(self):
        form = await self.request.form()
        self.name = form.get("name")
        self.email = form.get("email")
        self.psw = form.get("psw")

    # def is_valid(self) -> bool:
    #     return all([self.username, self.email, self.password])