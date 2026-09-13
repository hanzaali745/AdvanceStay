from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime
from typing import List

from database.models import Article, Author, AnalyticsEvent
from database.schemas import ArticleResponse, ArticleDetailResponse, ArticleCreate, ArticleUpdate
from config import settings
from api.auth import get_current_user

router = APIRouter(prefix="/api/articles", tags=["articles"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict)
def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
    category: str = Query(None),
    difficulty: str = Query(None),
    sort: str = Query("newest"),
    db: Session = Depends(get_db)
):
    """List all published articles with pagination and filtering"""
    query = db.query(Article).filter(Article.is_published == True)

    if category:
        query = query.filter(Article.category == category)

    if difficulty:
        query = query.filter(Article.difficulty == difficulty)

    # Sorting
    if sort == "newest":
        query = query.order_by(desc(Article.created_at))
    elif sort == "trending":
        query = query.order_by(Article.trending_rank.asc())
    elif sort == "difficulty":
        order_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
        query = query.order_by(
            func.case((Article.difficulty == "beginner", 1),
                     (Article.difficulty == "intermediate", 2),
                     (Article.difficulty == "advanced", 3), else_=4)
        )
    elif sort == "verified":
        query = query.order_by(desc(Article.confidence_score))

    total = query.count()

    articles = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "articles": [ArticleResponse.from_orm(a) for a in articles]
    }

@router.get("/{article_id}", response_model=ArticleDetailResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get full article by ID"""
    article = db.query(Article).filter(Article.id == article_id).first()

    if not article or not article.is_published:
        raise HTTPException(status_code=404, detail="Article not found")

    return article

@router.get("/slug/{slug}", response_model=ArticleDetailResponse)
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get full article by slug"""
    article = db.query(Article).filter(
        (Article.slug == slug) & (Article.is_published == True)
    ).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return article

@router.post("", response_model=ArticleResponse, status_code=201)
def create_article(
    article: ArticleCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new article (admin only)"""
    # TODO: Add admin check
    author = db.query(Author).filter(Author.id == article.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    new_article = Article(
        title=article.title,
        slug=article.slug,
        content=article.content,
        excerpt=article.excerpt,
        author_id=article.author_id,
        category=article.category,
        difficulty=article.difficulty,
        image_url=article.image_url,
        confidence_score=article.confidence_score,
        tags=article.tags,
        is_published=False
    )

    db.add(new_article)
    db.commit()
    db.refresh(new_article)

    return new_article

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article(
    article_id: int,
    update: ArticleUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update article (admin only)"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if update.title is not None:
        article.title = update.title
    if update.excerpt is not None:
        article.excerpt = update.excerpt
    if update.content is not None:
        article.content = update.content
    if update.category is not None:
        article.category = update.category
    if update.difficulty is not None:
        article.difficulty = update.difficulty
    if update.image_url is not None:
        article.image_url = update.image_url
    if update.confidence_score is not None:
        article.confidence_score = update.confidence_score
    if update.is_published is not None:
        article.is_published = update.is_published
        if update.is_published and not article.published_at:
            article.published_at = datetime.utcnow()
    if update.tags is not None:
        article.tags = update.tags

    article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(article)

    return article

@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete article (admin only)"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()

    return None

@router.get("/category/{category}", response_model=dict)
def get_articles_by_category(
    category: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size),
    db: Session = Depends(get_db)
):
    """Get articles by category"""
    query = db.query(Article).filter(
        (Article.category == category) & (Article.is_published == True)
    )

    total = query.count()
    articles = query.order_by(desc(Article.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "articles": [ArticleResponse.from_orm(a) for a in articles]
    }

@router.post("/{article_id}/view")
def track_article_view(article_id: int, db: Session = Depends(get_db)):
    """Track article view"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.view_count += 1

    event = AnalyticsEvent(
        event_type="page_view",
        article_id=article_id,
        metadata={"timestamp": datetime.utcnow().isoformat()}
    )

    db.add(event)
    db.commit()

    return {"view_count": article.view_count}

@router.post("/{article_id}/read")
def mark_article_read(article_id: int, db: Session = Depends(get_db)):
    """Mark article as read"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article.read_count += 1

    event = AnalyticsEvent(
        event_type="article_read",
        article_id=article_id,
        metadata={"timestamp": datetime.utcnow().isoformat()}
    )

    db.add(event)
    db.commit()

    return {"read_count": article.read_count}
