from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from typing import Optional
from enum import Enum

from datetime import datetime, timezone
import uuid

class AnalysisStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    complete = "complete"
    failed = "failed"

class Analysis(SQLModel, table=True):
    # IDs
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)

    # Time
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    status: AnalysisStatus = Field(default=AnalysisStatus.pending)

    # File
    filename: str
    file_path: str

    # Analysis config
    analysis_type: str
    parameters: dict = Field(default_factory=dict, sa_column=Column(JSON))

    # Results
    results: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    error: Optional[str] = None