import logging

from fastapi import Request
from fastapi.responses import JSONResponse


async def value_error_handler(request: Request, exc: ValueError):
    logger = logging.getLogger(__name__)
    logger.error(f"ValueError occurred: {str(exc)}")

    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
