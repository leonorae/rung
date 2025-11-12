from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Data Paths
    example_dir: Path = Path("data/examples")
    upload_dir: Path = Path("data/uploads")

    class Config:
        env_file = ".env"

settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)