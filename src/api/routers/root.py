from fastapi import APIRouter

from src.core.settings import get_app_settings

router = APIRouter()


@router.get("/settings", name="root:settings")
async def get_app_info():
    settings = get_app_settings()
    info = {
        "api_prefix": settings.prefixes.api_prefix,
        # "postgres_dsn": settings.postgres_dsn,
        # "redis_dsn": settings.redis_dsn,
        "fastapi_kwargs": settings.fastapi_kwargs,
    }

    return info

# @router.get("/logger", name="core:logger")
# async def logger_test():
#     logger.trace("This is logger.trace call")
#     logger.debug("This is logger.debug call")
#     logger.info("This is logger.info call")
#     logger.success("This is logger.success call")
#     logger.warning("This is logger.warning call")
#     logger.error("This is logger.error call")
#     logger.critical("This is logger.critical call")
#
#     return {"message": "OK"}
