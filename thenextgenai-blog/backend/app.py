from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from datetime import datetime
import logging

from config import settings
from database.models import Base
from database import models

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="The Next Gen AI API",
    description="Backend API for The Next Gen AI blog platform",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "3.0.0"
    }

# Root endpoint
@app.get("/")
def root():
    return {
        "name": "The Next Gen AI API",
        "version": "3.0.0",
        "docs": "/docs",
        "status": "operational"
    }

# TODO: Import and include routers
# from api import auth, articles, authors, search, newsletter, bookmarks, analytics

# Include routers (when created)
# app.include_router(auth.router)
# app.include_router(articles.router)
# app.include_router(authors.router)
# app.include_router(search.router)
# app.include_router(newsletter.router)
# app.include_router(bookmarks.router)
# app.include_router(analytics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
