from starlette.applications import Starlette


def add_middleware(app: Starlette, middleware_type: any, *args, **kwargs):
    app.add_middleware(
        middleware_type,
        *args,
        **kwargs,
    )
