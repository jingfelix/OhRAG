from fastapi import FastAPI

from app.database.models import init_db


def create_app():
    app = FastAPI()

    init_db()
    from app.routers import namespace

    app.include_router(namespace.router)

    return app


app = create_app()
