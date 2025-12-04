from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException, Form
from sqlmodel import Session, select
from typing import List, Optional
import uuid

from bnlearn import import_example
from rung.config import settings
from rung.database import get_session
from rung.schemas.analysis import Analysis
from rung.services.analysis import create_analysis_record, process_analysis
router = APIRouter()
@router.post("/upload", response_model=Analysis)
async def create_analysis_from_upload(
        file: UploadFile = File(...),
        preprocess_type: Optional[str] = Form("onehot"),
        analysis_type: str = Form("discovery"),
        method: Optional[str] = Form("pc"),
        alpha: Optional[float] = Form(0.05),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        session: Session = Depends(get_session)
):
    """Write uploaded file, track job in DB, and run analysis service"""
    # Generate a new uuid (for now: file and analysis have the same ID, no file caching/specification)
    analysis_uuid = str(uuid.uuid4())

    file_path = settings.upload_dir / f"{analysis_uuid}_{file.filename}"

    # write the file to local storage
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # create the parameter dictionary
    parameters = {"preprocess_type": preprocess_type,
                  "method": method}

    match analysis_type:
        case "discovery":
            parameters["alpha"] = alpha

    # if file uuid and job uuid are separated in future, this function will generate it with default parameter
    analysis = create_analysis_record(file.filename,
                                      str(file_path),
                                      preprocess_type,
                                      analysis_type,
                                      method,
                                      parameters,
                                      session,
                                      analysis_uuid)

    background_tasks.add_task(process_analysis, analysis.uuid)

    return analysis

@router.post("/example", response_model=Analysis)
def create_analysis_from_example(
        example_set: str = Form(...),
        example_name: str = Form(...),
        analysis_type: str = Form("discovery"),
        method: Optional[str] = Form("pc"),
        alpha: Optional[float] = Form(0.05),
        background_tasks: BackgroundTasks = BackgroundTasks(),
        session: Session = Depends(get_session)
):

    match example_set:
        case "rung":
            pass
        case "bnlearn":
            df_raw = import_example(data='titanic')



    analysis_uuid = str(uuid.uuid4())
    file_path = settings.example_dir / f"{analysis_uuid}_{example_name}"

    parameters = {}
    if analysis_type == "discovery":
        parameters["method"] = method
        parameters["alpha"] = alpha

    analysis = create_analysis_record(example_name,
                                      str(file_path),
                                      analysis_type,
                                      parameters,
                                      session,
                                      analysis_uuid)

    background_tasks.add_task(process_analysis, analysis.uuid)

    return analysis


@router.get("/{analysis_uuid}", response_model=Analysis)
def get_analysis(analysis_uuid: str,
                 session: Session = Depends(get_session)):

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