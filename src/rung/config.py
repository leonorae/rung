from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Data Paths
    example_dir: Path = Path("data/examples")
    upload_dir: Path = Path("data/uploads")
    model_dir: Path = Path("data/models")

    database_url: str = "sqlite:///./rung.db"

    max_upload_size_mb: int = 100

    class Config:
        env_file = ".env"

settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)