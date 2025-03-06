from fastapi import APIRouter
from pydantic import BaseModel

from src.api.dependencies import SettingsDependency
from src.core.settings import FastAPISettings

router = APIRouter()


class AppInfoResponseSchema(BaseModel):
    api_prefix: str
    postgres_dsn: str
    redis_dsn: str
    fastapi_kwargs: FastAPISettings


@router.get("/settings", name="root:settings", response_model=AppInfoResponseSchema)
async def get_app_info(settings: SettingsDependency) -> AppInfoResponseSchema:
    return AppInfoResponseSchema(
        api_prefix=settings.api_prefix,
        postgres_dsn=settings.postgres_dsn,
        redis_dsn=settings.redis_dsn,
        fastapi_kwargs=settings.fastapi_kwargs,
    )

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
