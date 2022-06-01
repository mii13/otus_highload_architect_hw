from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from starlette.responses import JSONResponse

from src.api import router


def create_app():
    application = FastAPI(title='chat', version="1")

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request,
                                           exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": exc.errors(), "body": exc.body}),
        )

    application.include_router(router.router)

    if 1:
        from opentelemetry import trace
        from opentelemetry.exporter.jaeger.proto.grpc import \
            JaegerExporter as GrpcJaegerExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        from opentelemetry.sdk.resources import Resource

        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor

        resource = Resource(attributes={"service.name": "fastapi-chat"})
        tracer = TracerProvider(resource=resource)
        trace.set_tracer_provider(tracer)

        tracer.add_span_processor(BatchSpanProcessor(GrpcJaegerExporter(
            collector_endpoint='jaeger-all-in-one:14250', insecure=True)))

        FastAPIInstrumentor.instrument_app(application, tracer_provider=tracer)

    return application


app = create_app()
