from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import ENV_PATH

settings_config_dict = SettingsConfigDict(
    env_file=ENV_PATH,
    env_file_encoding='utf-8',
    validate_default=False,
    extra="ignore",
)


class SettingsModel(BaseSettings):
    model_config = settings_config_dict


class FastAPISettings(BaseModel):
    debug: bool = True
    api_prefix: str = "/api"
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI pet project"
    version: str = "0.1.0"


class LoggingSettings(BaseModel):
    file: str = "backend.log"
    rotation: str = "2MB"
    compression: str = "zip"


class CorsMiddlewareSettings(BaseModel):
    allow_origins: list[str] = ["*"]
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]


class Settings(BaseModel):
    # auth: AuthSettings = AuthSettings()
    # redis: RedisSettings = RedisSettings()
    # postgres: PostgresSettings = PostgresSettings()

    fastapi: FastAPISettings = FastAPISettings()
    logging: LoggingSettings = LoggingSettings()
    cors_middleware: CorsMiddlewareSettings = CorsMiddlewareSettings()

    # @property
    # def postgres_dsn(self) -> PostgresDsn:
    #     return (
    #         f"postgresql+asyncpg://"
    #         f"{self.postgres.user}:{self.postgres.password}@"
    #         f"{self.postgres.host}:{self.postgres.port}/"
    #         f"{self.postgres.name}"
    #     )
    #
    # @property
    # def redis_dsn(self) -> RedisDsn:
    #     return f"redis://{self.redis.host}:{self.redis.port}"

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return self.fastapi.model_dump()

    @property
    def cors_middleware_kwargs(self) -> dict[str, any]:
        return self.cors_middleware.model_dump()


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
