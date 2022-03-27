from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse
from config import settings

from src.api import router


def get_app():
    print(settings)
    fastapi_params = dict(
        title="social network",
        version="1",
        # on_startup=signals.startup_callbacks,
        # exception_handlers=middleware.exception_handlers,
    )
    if settings.is_production:
        # docs is behind password
        app = FastAPI(**fastapi_params, docs_url=None, redoc_url=None,
                      openapi_url=None)
    else:
        # docs is open
        app = FastAPI(**fastapi_params, debug=True)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request,
                                           exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": exc.errors(), "body": exc.body}),
        )

    app.include_router(router.router)

    return app


app = get_app()
