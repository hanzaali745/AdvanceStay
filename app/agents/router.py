from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.agents.orchestrator import run_full_pipeline
from app.database import get_db

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/run")
def trigger_pipeline_run(db: Session = Depends(get_db)):
    run_full_pipeline(db)
    return RedirectResponse(url="/", status_code=303)
