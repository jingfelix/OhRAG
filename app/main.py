from fastapi import FastAPI

from app.database.models import init_db


def create_app():
    app = FastAPI()

    init_db()
    from app.routers import chunk, document, namespace

    app.include_router(namespace.router)
    app.include_router(document.router)
    app.include_router(chunk.router)

    return app


app = create_app()
