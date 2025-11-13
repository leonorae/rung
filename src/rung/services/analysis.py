from sqlmodel import Session, select
from datetime import datetime
import pandas as pd

from rung.schemas.analysis import Analysis
from rung.database import engine

def process_analysis(analysis_id: str):
    """analysis background service"""
    with Session(engine) as session:
        analysis = session.get(Analysis, analysis_id)

        if analysis and (analysis.status=="pending"):
            try:
                analysis.status = "processing"
                session.add(analysis)
                session.commit()

                df = pd.read_sql(analysis.file_path)

                results = {
                    "rows": len(df),
                    "columns": len(df.columns),
                }

                analysis.status = "complete"
                analysis.results = results

            except Exception as e:
                analysis.status = "failed"
                analysis.error = str(e)

            finally:
                session.add(analysis)
                session.commit()