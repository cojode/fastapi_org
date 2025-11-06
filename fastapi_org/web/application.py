from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from fastapi_org.web.api.router import api_router
from fastapi_org.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="fastapi_org",
        version=metadata.version("fastapi_org"),
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.include_router(router=api_router, prefix="/api")

    return app
