import os
import uvicorn

from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from database import engine, Base
from routers import items, health

load_dotenv(Path(__file__).parent / ".env")




@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="DevOps Lab API", lifespan=lifespan)

app.include_router(health.router)
app.include_router(items.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=True)
