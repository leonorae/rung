from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException, Form
from sqlmodel import Session, select
from typing import List, Optional
import uuid

from rung.config import settings
from rung.database import get_session
from rung.schemas.analysis import Analysis
from rung.services.analysis import process_analysis
router = APIRouter()
@router.post("/", response_model=Analysis)
async def create_analysis(
        file: UploadFile = File(...),
        analysis_type: str = Form("discovery"),
        method: Optional[str] = Form("pc"),
        alpha: Optional[float] = Form(0.05),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        session: Session = Depends(get_session)
):
    """Write uploaded file, track job in DB, and run analysis service"""
    file_uuid = str(uuid.uuid4())
    file_path = settings.upload_dir / f"{file_uuid}_{file.filename}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    parameters = {}
    if analysis_type == "discovery":
        parameters["method"] = method
        parameters["alpha"] = alpha

    analysis = Analysis(
        filename=file.filename,
        analysis_type=analysis_type,
        parameters=parameters,
        file_path=str(file_path),
        status="pending"
    )

    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    background_tasks.add_task(process_analysis, analysis.uuid)

    return analysis

@router.get("/{analysis_uuid}", response_model=Analysis)
def get_analysis(analysis_uuid: str, session: Session = Depends(get_session)):
    analysis = session.get(Analysis, analysis_uuid)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/", response_model=List[Analysis])
def list_analyses(session: Session = Depends(get_session)):
    """List all analyses"""
    statement = select(Analysis).order_by(Analysis.created_at)
    analyses = session.exec(statement).all()
    return analyses