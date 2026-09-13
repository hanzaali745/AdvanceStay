from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.models import Author, Article
from database.schemas import AuthorResponse, AuthorCreate
from config import settings

router = APIRouter(prefix="/api/authors", tags=["authors"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=dict)
def list_authors(
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size),
    db: Session = Depends(get_db)
):
    """List all authors"""
    query = db.query(Author)
    total = query.count()

    authors = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "authors": [AuthorResponse.from_orm(a) for a in authors]
    }

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get author by ID"""
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@router.get("/slug/{slug}", response_model=AuthorResponse)
def get_author_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get author by slug"""
    author = db.query(Author).filter(Author.slug == slug).first()

    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    return author

@router.post("", response_model=AuthorResponse, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Create new author (admin only)"""
    existing = db.query(Author).filter(Author.slug == author.slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Author slug already exists")

    new_author = Author(
        name=author.name,
        slug=author.slug,
        title=author.title,
        affiliation=author.affiliation,
        bio=author.bio,
        email=author.email,
        twitter=author.twitter,
        github=author.github,
        website=author.website
    )

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author

@router.get("/{author_id}/articles", response_model=dict)
def get_author_articles(
    author_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(settings.default_page_size),
    db: Session = Depends(get_db)
):
    """Get all articles by an author"""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    query = db.query(Article).filter(
        (Article.author_id == author_id) & (Article.is_published == True)
    )

    total = query.count()
    articles = query.order_by(desc(Article.created_at)).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return {
        "author": AuthorResponse.from_orm(author),
        "total": total,
        "page": page,
        "articles": articles
    }
