from fastapi import APIRouter

from src.api.routers import root

router = APIRouter()

router.include_router(root.router, tags=["Root"], prefix="/root")

__all__ = [
    "router",
]
