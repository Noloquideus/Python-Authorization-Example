from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api.auth import auth_router


@asynccontextmanager
async def lifespan(_):
    print("startup")
    yield
    print("shutdown")


app = FastAPI(title='Auth Service', description='Auth Service API', version='1.0.0', redoc_url=None, lifespan=lifespan)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Auth service"}
