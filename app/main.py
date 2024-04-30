from fastapi import FastAPI
from .routers import enigma_I
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


root_path = "enigma-api"
api_version = "v1"

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app = FastAPI(
        prefix="/{root_path}/{api_version}/enigma".format(root_path = root_path, api_version = api_version)
    )
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(enigma_I.router)