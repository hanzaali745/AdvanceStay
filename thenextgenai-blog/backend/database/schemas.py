from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str]
    tier: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Author Schemas
class AuthorBase(BaseModel):
    name: str
    slug: str
    title: Optional[str] = None
    affiliation: Optional[str] = None
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    email: Optional[str] = None
    twitter: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    avatar_url: Optional[str]
    email: Optional[str]
    twitter: Optional[str]
    github: Optional[str]
    website: Optional[str]
    verification_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    difficulty: str = "intermediate"
    image_url: Optional[str] = None
    confidence_score: int = 0
    tags: Optional[List[str]] = None

class ArticleCreate(ArticleBase):
    content: str
    author_id: int

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    image_url: Optional[str] = None
    confidence_score: Optional[int] = None
    is_published: Optional[bool] = None
    tags: Optional[List[str]] = None

class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    author: Optional[AuthorResponse] = None
    confidence_score: int
    trending_rank: Optional[int]
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_published: bool
    view_count: int
    read_count: int

    class Config:
        from_attributes = True

class ArticleDetailResponse(ArticleResponse):
    content: str

# Newsletter Schemas
class NewsletterSubscribeRequest(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    frequency: str = "weekly"

class NewsletterSubscriberResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    is_verified: bool
    frequency: str
    subscribed_at: datetime

    class Config:
        from_attributes = True

# Auth Schemas
class TokenRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    password: str

# Bookmark Schemas
class BookmarkCreate(BaseModel):
    article_id: int

class BookmarkResponse(BaseModel):
    id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Search Schemas
class SearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    difficulty: Optional[str] = None
    author_id: Optional[int] = None
    page: int = 1
    page_size: int = 20

class SearchResult(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: Optional[str]
    author: Optional[AuthorResponse]
    category: Optional[str]
    difficulty: str
    image_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[SearchResult]

# Analytics Schemas
class AnalyticsEventRequest(BaseModel):
    event_type: str
    article_id: Optional[int] = None
    metadata: Optional[dict] = None

class AnalyticsEventResponse(BaseModel):
    id: int
    event_type: str
    created_at: datetime

    class Config:
        from_attributes = True

# Trending Schemas
class TrendingArticleResponse(ArticleResponse):
    trending_rank: int
    view_count: int
    read_count: int

# Error Response
class ErrorResponse(BaseModel):
    detail: str
    code: Optional[str] = None
