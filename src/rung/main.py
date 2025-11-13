from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from contextlib import asynccontextmanager

from rung.config import settings

engine = create_engine(settings.database_url, echo=True)

import rung.api.analyses as analyses

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup

    # End startup
    yield
    # Cleanup
app = FastAPI(
    title="Rung",
    description="causal lab",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(analyses.router)
@app.get("/")
def read_root():
    return {"Hello": "World"}