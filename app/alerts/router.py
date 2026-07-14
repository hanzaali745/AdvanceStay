from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.database.models import Alert
from app.templating import templates

router = APIRouter()


@router.get("/alerts")
def list_alerts(request: Request, db: Session = Depends(get_db)):
    alerts = db.execute(select(Alert).order_by(Alert.created_at.desc())).scalars().all()
    return templates.TemplateResponse("alerts/list.html", {"request": request, "alerts": alerts})


@router.post("/alerts/{alert_id}/read")
def mark_read(alert_id: int, db: Session = Depends(get_db)):
    alert = db.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_read = True
    db.commit()
    return RedirectResponse(url="/alerts", status_code=303)
