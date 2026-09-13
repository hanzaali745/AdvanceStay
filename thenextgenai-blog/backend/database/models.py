from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Index, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(500))
    bio = Column(Text)
    tier = Column(String(50), default="free")  # free, pro, enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)

    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    reading_history = relationship("ReadingHistory", back_populates="user", cascade="all, delete-orphan")
    analytics_events = relationship("AnalyticsEvent", back_populates="user")

    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_username", "username"),
    )


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    avatar_url = Column(String(500))
    bio = Column(Text)
    title = Column(String(255))
    affiliation = Column(String(255))
    email = Column(String(255))
    twitter = Column(String(255))
    github = Column(String(255))
    website = Column(String(500))
    verification_status = Column(String(50), default="unverified")  # unverified, verified, expert
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    articles = relationship("Article", back_populates="author")

    __table_args__ = (
        Index("idx_author_slug", "slug"),
    )


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)  # Markdown content
    excerpt = Column(Text)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    category = Column(String(100))  # research, tutorials, guides, analysis
    difficulty = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    image_url = Column(String(500))
    confidence_score = Column(Integer, default=0)  # 0-100
    trending_rank = Column(Integer)
    tags = Column(JSON)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = Column(Boolean, default=False, index=True)
    view_count = Column(Integer, default=0)
    read_count = Column(Integer, default=0)

    author = relationship("Author", back_populates="articles")
    bookmarks = relationship("Bookmark", back_populates="article", cascade="all, delete-orphan")
    reading_history = relationship("ReadingHistory", back_populates="article", cascade="all, delete-orphan")
    analytics_events = relationship("AnalyticsEvent", back_populates="article")

    __table_args__ = (
        Index("idx_article_slug", "slug"),
        Index("idx_article_category", "category"),
        Index("idx_article_author_id", "author_id"),
        Index("idx_article_is_published", "is_published"),
        Index("idx_article_created_at", "created_at"),
    )


class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime)
    is_active = Column(Boolean, default=True, index=True)
    verification_token = Column(String(255))
    is_verified = Column(Boolean, default=False)
    frequency = Column(String(50), default="weekly")  # daily, weekly, monthly

    __table_args__ = (
        Index("idx_newsletter_email", "email"),
        Index("idx_newsletter_is_active", "is_active"),
    )


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookmarks")
    article = relationship("Article", back_populates="bookmarks")

    __table_args__ = (
        Index("idx_bookmark_user_article", "user_id", "article_id"),
    )


class ReadingHistory(Base):
    __tablename__ = "reading_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    scroll_position = Column(Integer, default=0)  # percentage
    read_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="reading_history")
    article = relationship("Article", back_populates="reading_history")

    __table_args__ = (
        Index("idx_reading_user_article", "user_id", "article_id"),
    )


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(100), nullable=False, index=True)  # page_view, article_read, search, signup, etc
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="SET NULL"))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="analytics_events")
    article = relationship("Article", back_populates="analytics_events")

    __table_args__ = (
        Index("idx_analytics_event_type", "event_type"),
        Index("idx_analytics_created_at", "created_at"),
    )
