from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.settings.service import OVERRIDABLE_NUMERIC_KEYS, get_effective_settings, set_setting
from app.templating import templates

router = APIRouter()


@router.get("/settings")
def settings_page(request: Request, db: Session = Depends(get_db)):
    effective = get_effective_settings(db)
    return templates.TemplateResponse("settings/index.html", {"request": request, "settings": effective})


@router.post("/settings")
async def save_settings(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    for key in OVERRIDABLE_NUMERIC_KEYS:
        if key in form and form[key] != "":
            set_setting(db, key, str(form[key]))
    return RedirectResponse(url="/settings", status_code=303)
