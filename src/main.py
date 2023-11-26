import logging

from fastapi import FastAPI

from core.settings import Settings
from api.router import router

settings = Settings()

app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=settings.openapi_documentation_url,
    docs_url=settings.api_documentation_url,
)
app.include_router(router, prefix="/api")


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
