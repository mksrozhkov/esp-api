# stdlib
import logging
from contextlib import asynccontextmanager

# thirdparty
from fastapi import FastAPI

# project
from src.config import settings
from src.log import init_sentry, setup_logging
from src.router import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_: FastAPI):
    """Замена deprecated @app.on_event("startup")$
    До yield - startup logic.
    После yield - shutdown logic.
    """
    setup_logging()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

# Включаем сентри
if settings.SENTRY_DSN:
    init_sentry()

# Добавляем роутер
app.include_router(router)
