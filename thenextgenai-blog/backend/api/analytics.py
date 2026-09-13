from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from database.models import AnalyticsEvent, Article, User
from database.schemas import AnalyticsEventResponse

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/event", response_model=dict, status_code=201)
def track_event(
    event_data: dict,
    db: Session = Depends(get_db)
):
    """Track an analytics event"""
    event = AnalyticsEvent(
        event_type=event_data.get("event_type"),
        user_id=event_data.get("user_id"),
        article_id=event_data.get("article_id"),
        metadata=event_data.get("metadata", {}),
        created_at=datetime.utcnow()
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {"event_id": event.id, "tracked": True}

@router.get("/user/{user_id}")
def get_user_analytics(
    user_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get analytics for a specific user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    cutoff = datetime.utcnow() - timedelta(days=days)

    events = db.query(AnalyticsEvent).filter(
        (AnalyticsEvent.user_id == user_id) &
        (AnalyticsEvent.created_at >= cutoff)
    ).all()

    event_counts = {}
    for event in events:
        event_type = event.event_type
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

    return {
        "user_id": user_id,
        "email": user.email,
        "period_days": days,
        "total_events": len(events),
        "event_breakdown": event_counts,
        "created_at": user.created_at.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None
    }

@router.get("/articles")
def get_articles_analytics(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get analytics for top articles"""
    cutoff = datetime.utcnow() - timedelta(days=days)

    articles = db.query(Article).filter(
        (Article.is_published == True) &
        (Article.created_at >= cutoff)
    ).order_by(Article.view_count.desc()).limit(limit).all()

    analytics = []
    for article in articles:
        events = db.query(AnalyticsEvent).filter(
            (AnalyticsEvent.article_id == article.id) &
            (AnalyticsEvent.created_at >= cutoff)
        ).all()

        analytics.append({
            "article_id": article.id,
            "title": article.title,
            "slug": article.slug,
            "views": article.view_count,
            "reads": article.read_count,
            "events": len(events),
            "confidence_score": article.confidence_score,
            "trending_rank": article.trending_rank
        })

    return {
        "period_days": days,
        "articles": analytics
    }

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    """Get overall analytics overview"""
    total_users = db.query(func.count(User.id)).scalar()
    total_articles = db.query(func.count(Article.id)).filter(
        Article.is_published == True
    ).scalar()
    total_views = db.query(func.sum(Article.view_count)).scalar() or 0
    total_reads = db.query(func.sum(Article.read_count)).scalar() or 0

    today = datetime.utcnow().date()
    today_events = db.query(AnalyticsEvent).filter(
        func.date(AnalyticsEvent.created_at) == today
    ).count()

    last_7_days = datetime.utcnow() - timedelta(days=7)
    week_events = db.query(AnalyticsEvent).filter(
        AnalyticsEvent.created_at >= last_7_days
    ).count()

    return {
        "total_users": total_users,
        "total_articles": total_articles,
        "total_views": total_views,
        "total_reads": total_reads,
        "today_events": today_events,
        "week_events": week_events,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/events")
def list_events(
    event_type: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List recent analytics events"""
    query = db.query(AnalyticsEvent)

    if event_type:
        query = query.filter(AnalyticsEvent.event_type == event_type)

    total = query.count()
    events = query.order_by(
        AnalyticsEvent.created_at.desc()
    ).offset(offset).limit(limit).all()

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "events": [AnalyticsEventResponse.from_orm(e) for e in events]
    }
