from sqlmodel import Session, select
from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import uuid

import pandas as pd

from rung.database import engine
from rung.schemas.analysis import Analysis, AnalysisStatus
from rung.causal.discovery import run_causal_discovery

def create_analysis_record(
        filename: str,
        file_path: str,
        analysis_type: str,
        parameters: Dict[str, Any],
        session: Session,
        analysis_uuid: str = str(uuid.uuid4()),
) -> Analysis:
    """Create a record of an analysis job and add it to the database"""

    analysis = Analysis(
        uuid=analysis_uuid,
        filename=filename,
        file_path=file_path,
        analysis_type=analysis_type,
        parameters=parameters,
        status="pending",
    )

    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    return analysis

def process_analysis(analysis_id: str):
    """analysis background service"""
    print(f"Background task started for {analysis_id}")
    with Session(engine) as session:
        analysis = session.get(Analysis, analysis_id)

        if not analysis:
            print(f"{analysis_id} not found")
            return
        try:
            analysis.status = AnalysisStatus.processing
            session.add(analysis)
            session.commit()

            df = pd.read_csv(analysis.file_path)


            if analysis.analysis_type == "discovery":
                method = analysis.parameters.get("method", "pc")
                alpha = analysis.parameters.get("alpha", 0.05)

                results = run_causal_discovery(
                    df,
                    method=method,
                    alpha=alpha
                )

                results["data_stats"] = {
                    "n_rows": len(df),
                    "n_columns": len(df.columns),
                    "columns": list(df.columns)
                }
            else:
                results = {
                    "error": f"Unknown analysis type: {analysis.analysis_type}"
                }


            analysis.status = AnalysisStatus.complete
            analysis.results = results

        except Exception as e:
            analysis.status = AnalysisStatus.failed
            analysis.error = str(e)

        finally:
            session.add(analysis)
            session.commit()