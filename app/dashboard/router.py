from fastapi import APIRouter, Depends, Request
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.agents.status import get_latest_agent_runs
from app.database import get_db
from app.database.models import Alert, Product, Supplier
from app.database.models.enums import Verdict
from app.inventory.service import summarise_inventory
from app.templating import templates

router = APIRouter()


@router.get("/")
def dashboard(request: Request, db: Session = Depends(get_db)):
    total_products = db.execute(select(func.count()).select_from(Product)).scalar_one()
    total_suppliers = db.execute(select(func.count()).select_from(Supplier)).scalar_one()
    watchlist_count = db.execute(
        select(func.count()).select_from(Product).where(Product.watchlist.is_(True))
    ).scalar_one()
    unread_alerts = db.execute(
        select(func.count()).select_from(Alert).where(Alert.is_read.is_(False))
    ).scalar_one()

    verdict_counts = dict(
        db.execute(select(Product.verdict, func.count()).group_by(Product.verdict)).all()
    )

    summaries = summarise_inventory(db)
    cash_invested = round(sum(s.cash_invested for s in summaries), 2)
    realised_profit = round(sum(s.realised_profit for s in summaries), 2)

    top_opportunities = db.execute(
        select(Product)
        .where(Product.verdict.in_([Verdict.BUY_NOW, Verdict.TEST_BUY]))
        .order_by(Product.confidence_score.desc().nulls_last())
        .limit(10)
    ).scalars().all()

    agent_runs = get_latest_agent_runs(db)

    return templates.TemplateResponse(
        "dashboard/index.html",
        {
            "request": request,
            "total_products": total_products,
            "total_suppliers": total_suppliers,
            "watchlist_count": watchlist_count,
            "unread_alerts": unread_alerts,
            "verdict_counts": verdict_counts,
            "cash_invested": cash_invested,
            "realised_profit": realised_profit,
            "top_opportunities": top_opportunities,
            "agent_runs": agent_runs,
        },
    )
