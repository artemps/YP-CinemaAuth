import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core import settings
from api.router import router

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=settings.openapi_documentation_url,
    docs_url=settings.api_documentation_url,
)
app.include_router(router, prefix="/api")


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host=settings.app_host,
        port=settings.app_port,
        log_config=settings.log_config,
        log_level=logging.DEBUG if settings.debug else logging.INFO,
        reload=settings.debug,
    )




