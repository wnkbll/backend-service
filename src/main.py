import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.config import Config
from src.core.toolkit import add_middleware
from src.routers import root


@asynccontextmanager
async def lifespan(_: FastAPI):
    ...
    yield
    ...


def get_application() -> FastAPI:
    config = Config()

    application = FastAPI(**config.fastapi_kwargs, lifespan=lifespan)

    application.include_router(root.router)

    add_middleware(application, CORSMiddleware, **config.cors_middleware_kwargs)

    return application


async def main():
    application = get_application()
    config = uvicorn.Config(
        application, host="127.0.0.1", port=8000, reload=True, reload_delay=0.25,
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())

# uvicorn --factory --reload --host 127.0.0.1 --port 8000 src.main:get_application
