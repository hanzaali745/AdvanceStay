from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, desc

from database.models import Article, Author
from database.schemas import SearchResponse, SearchResult
from config import settings

router = APIRouter(prefix="/api/search", tags=["search"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=SearchResponse)
def search_articles(
    q: str = Query(..., min_length=1, max_length=200),
    category: str = Query(None),
    difficulty: str = Query(None),
    author_id: int = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size),
    db: Session = Depends(get_db)
):
    """Full-text search across articles"""
    # Search in title, excerpt, and tags
    search_query = db.query(Article).filter(Article.is_published == True)

    # Full-text search filter
    search_filter = or_(
        Article.title.ilike(f"%{q}%"),
        Article.excerpt.ilike(f"%{q}%"),
        Article.content.ilike(f"%{q}%")
    )

    search_query = search_query.filter(search_filter)

    # Additional filters
    if category:
        search_query = search_query.filter(Article.category == category)

    if difficulty:
        search_query = search_query.filter(Article.difficulty == difficulty)

    if author_id:
        search_query = search_query.filter(Article.author_id == author_id)

    total = search_query.count()

    # Relevance scoring: boost title matches
    articles = search_query.order_by(
        desc(Article.created_at)
    ).offset((page - 1) * page_size).limit(page_size).all()

    results = []
    for article in articles:
        author = db.query(Author).filter(Author.id == article.author_id).first()
        result = SearchResult(
            id=article.id,
            title=article.title,
            slug=article.slug,
            excerpt=article.excerpt,
            author=author,
            category=article.category,
            difficulty=article.difficulty,
            image_url=article.image_url,
            created_at=article.created_at
        )
        results.append(result)

    return SearchResponse(
        total=total,
        page=page,
        page_size=page_size,
        results=results
    )

@router.get("/suggestions")
def search_suggestions(
    q: str = Query(..., min_length=1, max_length=50),
    db: Session = Depends(get_db)
):
    """Get search suggestions"""
    suggestions = db.query(Article.title).filter(
        (Article.title.ilike(f"%{q}%")) & (Article.is_published == True)
    ).distinct().limit(10).all()

    return {
        "suggestions": [s[0] for s in suggestions]
    }

@router.get("/trending-queries")
def trending_searches(db: Session = Depends(get_db)):
    """Get trending search queries (placeholder)"""
    return {
        "trending": [
            "LLMs",
            "Transformers",
            "Prompt Engineering",
            "Neural Networks",
            "Machine Learning"
        ]
    }
