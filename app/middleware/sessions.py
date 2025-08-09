# from starlette.middleware.sessions import SessionMiddleware
#
# def register_session(app, secret_key: str):
#     app.add_middleware(SessionMiddleware, secret_key=secret_key)

from fastapi import Request

def flash(request: Request, message: str, category: str = "info"):
    if "_flashes" not in request.session:
        request.session["_flashes"] = []
    request.session["_flashes"].append((category, message))

def get_flashed_messages(request: Request) -> list[tuple[str, str]]:
    return request.session.pop("_flashes", [])