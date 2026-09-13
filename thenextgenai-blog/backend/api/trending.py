from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.models import Article
from database.schemas import TrendingArticleResponse
from services.trending import trending_service
from config import settings

router = APIRouter(prefix="/api/trending", tags=["trending"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict)
def get_trending_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending articles"""
    articles = trending_service.get_trending_articles(db, limit=limit)

    return {
        "trending": [TrendingArticleResponse.from_orm(a) for a in articles]
    }

@router.post("/recalculate")
def recalculate_trending(db: Session = Depends(get_db)):
    """Manually recalculate trending scores (admin only)"""
    count = trending_service.recalculate_all_trending(db)
    return {
        "message": f"Recalculated trending for {count} articles",
        "count": count
    }

@router.get("/top")
def get_top_articles(
    days: int = Query(7, ge=1, le=90),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get top articles from past N days"""
    from datetime import datetime, timedelta

    cutoff = datetime.utcnow() - timedelta(days=days)

    articles = db.query(Article).filter(
        (Article.is_published == True) &
        (Article.created_at >= cutoff)
    ).order_by(
        Article.view_count.desc()
    ).limit(limit).all()

    return {
        "period_days": days,
        "articles": [TrendingArticleResponse.from_orm(a) for a in articles]
    }

@router.get("/by-category/{category}")
def get_trending_by_category(
    category: str,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get trending articles in a specific category"""
    articles = db.query(Article).filter(
        (Article.category == category) &
        (Article.is_published == True) &
        (Article.trending_rank.isnot(None))
    ).order_by(
        Article.trending_rank.asc()
    ).limit(limit).all()

    return {
        "category": category,
        "trending": [TrendingArticleResponse.from_orm(a) for a in articles]
    }

@router.get("/score/{article_id}")
def get_article_score(article_id: int, db: Session = Depends(get_db)):
    """Get detailed trending score breakdown for an article"""
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        return {"error": "Article not found"}

    score = trending_service.calculate_trending_score(article, db)

    return {
        "article_id": article_id,
        "title": article.title,
        "score": score,
        "ranking_factors": {
            "view_count": article.view_count,
            "read_count": article.read_count,
            "trending_rank": article.trending_rank,
            "confidence_score": article.confidence_score,
            "created_at": article.created_at.isoformat()
        }
    }
