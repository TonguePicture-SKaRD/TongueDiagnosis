from .user_api import router_user


def register_routes(app):
    app.include_router(router_user, prefix="/api/user")
