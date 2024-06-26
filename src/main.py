from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from src.api.routing.auth import auth_router
from src.infrastructure.cache.redis import init_redis
from src.infrastructure.utils.init_superadmin import create_superadmin


@asynccontextmanager
async def lifespan(_):
    await init_redis()
    await create_superadmin()
    print("startup")
    yield
    print("shutdown")


app = FastAPI(title='Auth Service', description='Auth Service API', version='1.0.0', redoc_url=None, lifespan=lifespan)
app.include_router(auth_router)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


@app.get("/")
async def root():
    return {"message": "Auth service"}
