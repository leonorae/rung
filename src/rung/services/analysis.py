from sqlmodel import Session, select
from datetime import datetime
import pandas as pd

from rung.schemas.analysis import Analysis, AnalysisStatus
from rung.database import engine

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

            results = {
                "rows": len(df),
                "columns": len(df.columns),
            }

            analysis.status = AnalysisStatus.complete
            analysis.results = results

        except Exception as e:
            analysis.status = AnalysisStatus.failed
            analysis.error = str(e)

        finally:
            session.add(analysis)
            session.commit()