import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.staticfiles import StaticFiles
import uvicorn
from redis import asyncio as aioredis

from Auth import User, get_user_manager, auth_backend, UserRead, UserCreate
from pages.router import router as router_pages
from operations.router import router as router_operation
from pages.router import router as router_pages


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # redis = aioredis.from_url("redis://localhost")
    # redis://[[username]:[password]]@localhost:6379/0
    redis = aioredis.from_url("redis://my_user:my_user_password@localhost:6380/0")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

# include config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operation)
# app.include_router(router_tasks)
app.include_router(router_pages)

current_user = fastapi_users.current_user()


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/unprotected-route")
async def unprotected_route():
    return "Hello, anonym"


@app.get("/long-operation")
@cache(expire=60)
async def long_operation():
    time.sleep(2)
    return {"return many data"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
