from fastapi import FastAPI
from contextlib import asynccontextmanager
from RogersComcastBackend.app.core import config, logging
from RogersComcastBackend.app.db.database import init_db
from RogersComcastBackend.app.routers.v1 import users, items

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.setup_logging()
    await init_db()
    yield

app = FastAPI(
    title="RogersComcastBackend",
    version="0.1.0",
    description="Rogers integration layer",
    lifespan=lifespan
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to RogersComcastBackend!"}