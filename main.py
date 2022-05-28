from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles

from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse

from src.api import router
from src.api.ws import start_ws_consume


def get_app():
    fastapi_params = dict(
        title="social network",
        version="1",
        on_startup=[start_ws_consume, ]
        # exception_handlers=middleware.exception_handlers,
    )
    app = FastAPI(**fastapi_params, docs_url=None, redoc_url=None,
                  openapi_url=None)
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

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
