from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import register_routes


def create_app():
    # create and configure the app
    app = FastAPI()

    origins = [
        "http://127.0.0.1:5173",
        "http://localhost:5173"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routes(app)

    @app.get("/hello")  # hello world页面
    def hello():
        return "Hello, World!"

    return app
