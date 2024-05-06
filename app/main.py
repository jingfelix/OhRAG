from fastapi import FastAPI

from app.database.models import init_db


def create_app():
    app = FastAPI()

    init_db()
    from app.routers import chunk, document, namespace, query

    app.include_router(namespace.router)
    app.include_router(document.router)
    app.include_router(chunk.router)
    app.include_router(query.router)

    from app.exceptions import common

    app.add_exception_handler(ValueError, common.value_error_handler)

    return app


app = create_app()
