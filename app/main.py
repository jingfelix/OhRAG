from fastapi import FastAPI

from app.database.models import init_db


def create_app():
    app = FastAPI()

    init_db()
    from app.routers import document, namespace

    app.include_router(namespace.router)
    app.include_router(document.router)

    return app


app = create_app()
