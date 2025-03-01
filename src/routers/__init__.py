from fastapi import APIRouter

from src.routers import home
from src.core.settings import get_app_settings


def get_head_router() -> APIRouter:
    config = get_app_settings()

    router = APIRouter()
    api_router = APIRouter(prefix=config.fastapi.api_prefix)

    router.include_router(home.router)
    router.include_router(api_router)

    return router
