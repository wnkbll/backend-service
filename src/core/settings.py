from functools import lru_cache

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn
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


class RedisSettings(SettingsModel):
    host: str = Field(default=None, validation_alias="REDIS_HOST")
    port: str = Field(default=None, validation_alias="REDIS_PORT")


class PostgresSettings(SettingsModel):
    user: str = Field(default=None, validation_alias="POSTGRES_USER")
    password: str = Field(default=None, validation_alias="POSTGRES_PASS")
    host: str = Field(default=None, validation_alias="POSTGRES_HOST")
    port: str = Field(default=None, validation_alias="POSTGRES_PORT")
    name: str = Field(default=None, validation_alias="POSTGRES_NAME")


class FastAPISettings(BaseModel):
    debug: bool = True
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
    api_prefix: str = "/api"

    # auth: AuthSettings = AuthSettings()
    redis: RedisSettings = RedisSettings()
    postgres: PostgresSettings = PostgresSettings()

    fastapi: FastAPISettings = FastAPISettings()
    logging: LoggingSettings = LoggingSettings()
    cors_middleware: CorsMiddlewareSettings = CorsMiddlewareSettings()

    @lru_cache
    @property
    def postgres_dsn(self) -> PostgresDsn:
        driver = "postgresql+asyncpg"
        user = f"{self.postgres.host}:{self.postgres.port}"
        connection_url = f"{self.postgres.host}:{self.postgres.port}"

        return PostgresDsn(
            f"{driver}://{user}@{connection_url}/{self.postgres.name}"
        )

    @lru_cache
    @property
    def redis_dsn(self) -> RedisDsn:
        return RedisDsn(
            f"redis://{self.redis.host}:{self.redis.port}"
        )

    @lru_cache
    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return self.fastapi.model_dump()

    @lru_cache
    @property
    def cors_middleware_kwargs(self) -> dict[str, any]:
        return self.cors_middleware.model_dump()


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
