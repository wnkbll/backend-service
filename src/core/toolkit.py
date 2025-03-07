from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


def add_middleware(app: Starlette, middleware_type: any, *args, **kwargs):
    app.add_middleware(
        middleware_type,
        *args,
        **kwargs,
    )
