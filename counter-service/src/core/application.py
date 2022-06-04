from fastapi import FastAPI
from src.api.router import router


def create_app() -> FastAPI:
    application = FastAPI(
        title="counter-service",
        openapi_url="/api/openapi.json",
    )

    application.include_router(router)

    return application
