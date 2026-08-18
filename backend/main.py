from contextlib import asynccontextmanager
from fastapi import FastAPI # type: ignore
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title='AI-powered Document Intelligence',
    lifespan=lifespan
)

app.include_router(router)
