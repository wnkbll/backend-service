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
    driver: str = Field(default="redis")
    username: str = Field(default=None, validation_alias="REDIS_USER")
    password: str = Field(default=None, validation_alias="REDIS_PASSWORD")
    host: str = Field(default=None, validation_alias="REDIS_HOST")
    port: int = Field(default=None, validation_alias="REDIS_PORT")
    database: str = Field(default=None, validation_alias="REDIS_DB")


class PostgresSettings(SettingsModel):
    driver: str = Field(default="postgresql+asyncpg")
    username: str = Field(default=None, validation_alias="POSTGRES_USER")
    password: str = Field(default=None, validation_alias="POSTGRES_PASSWORD")
    host: str = Field(default=None, validation_alias="POSTGRES_HOST")
    port: int = Field(default=None, validation_alias="POSTGRES_PORT")
    database: str = Field(default=None, validation_alias="POSTGRES_DB")


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

    @property
    def postgres_dsn(self) -> str:
        return PostgresDsn.build(
            scheme=self.postgres.driver,
            username=self.postgres.username,
            password=self.postgres.password,
            host=self.postgres.host,
            port=self.postgres.port,
            path=self.postgres.database,
        ).unicode_string()

    @property
    def redis_dsn(self) -> str:
        return RedisDsn.build(
            scheme=self.redis.driver,
            username=self.redis.username,
            password=self.redis.password,
            host=self.redis.host,
            port=self.redis.port,
            path=self.redis.database,
        ).unicode_string()

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return self.fastapi.model_dump()

    @property
    def cors_middleware_kwargs(self) -> dict[str, any]:
        return self.cors_middleware.model_dump()


@lru_cache
def get_app_settings() -> Settings:
    return Settings()
