# from starlette.middleware.sessions import SessionMiddleware
#
# def register_session(app, secret_key: str):
#     app.add_middleware(SessionMiddleware, secret_key=secret_key)

from fastapi import Request

#  Сохраняет flash-сообщение в сессии, сообщение сохраняется в cookie
# category — может быть "info", "success", "error" и т.д. Используется для CSS-классов.
def flash(request: Request, message: str, category: str = "info"):
    if "_flashes" not in request.session:
        request.session["_flashes"] = []
    request.session["_flashes"].append((category, message))

def get_flashed_messages(request: Request) -> list[tuple[str, str]]:
    # удаляет список сообщений из сессии и возвращает его. Если сообщений нет, возвращает пустой список
    return request.session.pop("_flashes", [])