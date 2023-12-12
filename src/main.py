import logging
import random

from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.router import router
from core import settings, limiter


app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=settings.openapi_documentation_url,
    docs_url=settings.api_documentation_url,
)
app.include_router(router)
app.add_middleware(SessionMiddleware, secret_key=random.randrange(0, 99999))
app.state.limiter = limiter.limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException) -> JSONResponse:
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




