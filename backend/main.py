from contextlib import asynccontextmanager
from fastapi import FastAPI # type: ignore
from app.api import upload, register_routes, login_routes, extract, history, document, delete


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title='AI-powered Document Intelligence',
    lifespan=lifespan
)

app.include_router(upload.router)
app.include_router(extract.router)
app.include_router(register_routes.router)
app.include_router(login_routes.router)
app.include_router(history.router)
app.include_router(document.router)
app.include_router(delete.router)
