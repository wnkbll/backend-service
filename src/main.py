from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.api.routers import router
from src.core.paths import TEMPLATES_PATH, STATIC_PATH
from src.core.settings import get_app_settings
from src.core.toolkit import add_middleware

settings = get_app_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    ...
    yield
    ...


app = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)
add_middleware(app, CORSMiddleware, **settings.cors_middleware_kwargs)

templates = Jinja2Templates(directory=TEMPLATES_PATH)
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

app.include_router(router, prefix=settings.api_prefix)


@app.get("/", name="root:home", tags=["Root"])
async def home(request: Request):
    return templates.TemplateResponse(request, "home.html")


if __name__ == "__main__":
    uvicorn.run(
        app, host="127.0.0.1", port=8000, reload=True,
    )
