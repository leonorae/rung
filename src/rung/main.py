from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from contextlib import asynccontextmanager

from rung.config import settings
from rung.database import engine
import rung.api.analyses as analyses

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created!")
    # End startup
    yield
    # Cleanup

app = FastAPI(
    title="Rung",
    description="causal lab",
    version="0.0.1",
    lifespan=lifespan
)

app.include_router(analyses.router, prefix="/api/analyses")
@app.get("/")
def read_root():
    return {"Hello": "World"}