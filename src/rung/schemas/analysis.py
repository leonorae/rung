from sqlmodel import SQLModel, Field
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
    id: Optional[int] = Field(default=None, primary_key=True)
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))


    # Time
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    status: AnalysisStatus = Field(default=AnalysisStatus.pending)

    # File
    filename: str
    file_path: str

    # Analysis config
    # analysis_type: str  # "discovery", "ate", etc.
    # parameters: dict = Field(default_factory=dict)

    # Results
    results: Optional[dict] = None
    error: Optional[str] = None