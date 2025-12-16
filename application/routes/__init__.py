from .user_api import router_user
from .model_api import router_tongue_analysis
from .ollama_used import *


def register_routes(app):
    app.include_router(router_user, prefix="/api/user")
    app.include_router(router_tongue_analysis, prefix="/api/model")
