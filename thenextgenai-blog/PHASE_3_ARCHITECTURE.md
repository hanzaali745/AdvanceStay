# Phase 3: Backend Infrastructure & API

## Overview
Phase 3 transforms the static frontend into a full-stack SaaS platform with:
- PostgreSQL database for persistent storage
- REST API for all operations
- User authentication and accounts
- Content management system (markdown-based)
- Email service integration
- Analytics and trending calculations
- Search functionality

## Architecture

```
backend/
├── app.py                 # FastAPI main application
├── requirements.txt       # Python dependencies
├── config.py             # Configuration (env-based)
├── database/
│   ├── __init__.py
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── migrations/       # Alembic migrations
│   └── seed.py           # Initial data
├── api/
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── articles.py       # Article CRUD
│   ├── authors.py        # Author profiles
│   ├── trending.py       # Trending calculation
│   ├── search.py         # Full-text search
│   ├── newsletter.py     # Newsletter signup
│   └── analytics.py      # User analytics
├── services/
│   ├── __init__.py
│   ├── email.py          # Email service
│   ├── content.py        # Content parsing (markdown)
│   ├── trending.py       # Trending algorithm
│   └── search.py         # Search engine
├── auth/
│   ├── __init__.py
│   ├── jwt.py            # JWT token management
│   └── password.py       # Password hashing
└── utils/
    ├── __init__.py
    └── helpers.py        # Common utilities
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  avatar_url VARCHAR(500),
  bio TEXT,
  tier VARCHAR(50) DEFAULT 'free',  -- free, pro, enterprise
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,
  last_login TIMESTAMP
);
```

### Authors Table
```sql
CREATE TABLE authors (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  avatar_url VARCHAR(500),
  bio TEXT,
  title VARCHAR(255),
  affiliation VARCHAR(255),
  email VARCHAR(255),
  twitter VARCHAR(255),
  github VARCHAR(255),
  website VARCHAR(500),
  verification_status VARCHAR(50) DEFAULT 'unverified',  -- unverified, verified, expert
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Articles Table
```sql
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  slug VARCHAR(500) UNIQUE NOT NULL,
  content TEXT NOT NULL,  -- Markdown content
  excerpt TEXT,
  author_id INT REFERENCES authors(id),
  category VARCHAR(100),  -- research, tutorials, guides, analysis
  difficulty VARCHAR(50) DEFAULT 'intermediate',  -- beginner, intermediate, advanced
  image_url VARCHAR(500),
  confidence_score INT DEFAULT 0,  -- 0-100
  trending_rank INT,
  tags JSONB,
  published_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_published BOOLEAN DEFAULT FALSE,
  view_count INT DEFAULT 0,
  read_count INT DEFAULT 0
);
```

### Newsletter Subscribers Table
```sql
CREATE TABLE newsletter_subscribers (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  subscribed_at TIMESTAMP DEFAULT NOW(),
  unsubscribed_at TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE,
  verification_token VARCHAR(255),
  is_verified BOOLEAN DEFAULT FALSE,
  frequency VARCHAR(50) DEFAULT 'weekly'  -- daily, weekly, monthly
);
```

### User Bookmarks Table
```sql
CREATE TABLE bookmarks (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  article_id INT REFERENCES articles(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, article_id)
);
```

### Reading History Table
```sql
CREATE TABLE reading_history (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  article_id INT REFERENCES articles(id) ON DELETE CASCADE,
  scroll_position INT DEFAULT 0,  -- percentage
  read_at TIMESTAMP DEFAULT NOW(),
  completed BOOLEAN DEFAULT FALSE
);
```

### Analytics Events Table
```sql
CREATE TABLE analytics_events (
  id SERIAL PRIMARY KEY,
  event_type VARCHAR(100),  -- page_view, article_read, search, signup, etc
  user_id INT REFERENCES users(id) ON DELETE SET NULL,
  article_id INT REFERENCES articles(id) ON DELETE SET NULL,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication
```
POST   /api/auth/register          # Create new account
POST   /api/auth/login             # Login user
POST   /api/auth/logout            # Logout
POST   /api/auth/refresh           # Refresh JWT token
POST   /api/auth/forgot-password   # Send password reset
POST   /api/auth/reset-password    # Reset password
GET    /api/auth/me                # Get current user
PUT    /api/auth/profile           # Update user profile
```

### Articles
```
GET    /api/articles               # List articles (paginated)
GET    /api/articles/{id}          # Get article by ID
GET    /api/articles/slug/{slug}   # Get article by slug
POST   /api/articles               # Create article (admin only)
PUT    /api/articles/{id}          # Update article (admin only)
DELETE /api/articles/{id}          # Delete article (admin only)
GET    /api/articles/category/{cat} # Get articles by category
GET    /api/articles/author/{author_id} # Get articles by author
GET    /api/articles/trending      # Get trending articles
POST   /api/articles/{id}/view     # Track article view
POST   /api/articles/{id}/read     # Mark article as read
```

### Authors
```
GET    /api/authors                # List all authors
GET    /api/authors/{id}           # Get author by ID
GET    /api/authors/slug/{slug}    # Get author by slug
PUT    /api/authors/{id}           # Update author (admin only)
GET    /api/authors/{id}/articles  # Get author's articles
```

### Search
```
GET    /api/search                 # Full-text search
GET    /api/search/suggestions     # Search suggestions
GET    /api/search/trending-queries # Popular searches
```

### Newsletter
```
POST   /api/newsletter/subscribe   # Subscribe to newsletter
POST   /api/newsletter/unsubscribe # Unsubscribe
POST   /api/newsletter/verify      # Verify email
GET    /api/newsletter/status      # Check subscription status
```

### Bookmarks (Authenticated)
```
POST   /api/bookmarks             # Add bookmark
DELETE /api/bookmarks/{id}        # Remove bookmark
GET    /api/bookmarks             # List user bookmarks
GET    /api/bookmarks/article/{id} # Check if bookmarked
```

### Analytics
```
POST   /api/analytics/event       # Track event
GET    /api/analytics/user        # Get user analytics
GET    /api/analytics/articles    # Get article analytics (admin)
```

## Trending Algorithm

### Scoring Factors
```
Score = (0.3 * View Count) + 
        (0.25 * Read Completion %) +
        (0.2 * Engagement Score) +
        (0.15 * Recency Factor) +
        (0.1 * Author Reputation)
```

### Calculation
- **View Count**: Total views in last 7 days
- **Read Completion**: % of readers who completed the article
- **Engagement**: Bookmarks, shares, comments (future phases)
- **Recency**: Newer articles weighted higher
- **Author Reputation**: Based on historical performance

### Updates
- Run every 6 hours
- Store in `articles.trending_rank`
- Exclude articles < 24 hours old
- Minimum 10 views to rank

## Email Service Integration

### Configuration (env-based)
```env
EMAIL_PROVIDER=sendgrid  # or mailgun, aws-ses
SENDGRID_API_KEY=xxxxx
FROM_EMAIL=editorial@thenextgenai.com
```

### Email Templates
```
templates/
├── welcome.html
├── newsletter_weekly.html
├── password_reset.html
├── article_published.html
└── engagement_digest.html
```

## Authentication Flow

### JWT Tokens
```
Access Token: 15 minutes
Refresh Token: 7 days
Cookie: httpOnly, Secure, SameSite=Strict
```

### Session Management
```python
def login(email, password):
    user = get_user_by_email(email)
    if verify_password(password, user.password_hash):
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return {access_token, refresh_token}
```

## Content Management

### Markdown Processing
```python
# articles/slug/understanding-llms.md
---
title: Understanding Large Language Models
author: Alex Rivera
category: research
difficulty: intermediate
image_url: https://unsplash.com/...
---

# Article content in markdown
## Section 1
Paragraph text...

## Section 2
More content...
```

### Content Parsing
- Parse YAML frontmatter
- Convert markdown to HTML
- Generate table of contents
- Extract metadata
- Build search index

## Search Implementation

### Full-Text Search
```sql
CREATE INDEX articles_search ON articles 
USING GIN (to_tsvector('english', title || ' ' || content));

SELECT * FROM articles 
WHERE to_tsvector('english', title || ' ' || content) 
@@ plainto_tsquery('english', 'search term')
ORDER BY ts_rank(...) DESC;
```

### Search Features
- Title + content search
- Author filtering
- Category filtering
- Date range filtering
- Difficulty level filtering
- Sorting: relevance, date, popularity

## Deployment Configuration

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost/thenextgenai
SQLALCHEMY_ECHO=False

# Security
SECRET_KEY=xxxxx
JWT_SECRET=xxxxx
JWT_ALGORITHM=HS256

# Email
EMAIL_PROVIDER=sendgrid
SENDGRID_API_KEY=xxxxx

# Frontend
FRONTEND_URL=https://thenextgenai.com
CORS_ORIGINS=["https://thenextgenai.com"]

# Analytics
ANALYTICS_ENABLED=True
```

### Docker Setup
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing Strategy

```
tests/
├── test_auth.py
├── test_articles.py
├── test_search.py
├── test_trending.py
├── test_email.py
└── fixtures/
    └── sample_data.sql
```

## Performance Considerations

1. **Database Indexing**
   - Index on `articles.slug`, `articles.category`, `articles.author_id`
   - Index on `users.email`, `users.username`
   - Full-text index on articles content

2. **Caching**
   - Cache trending articles (6 hours)
   - Cache author profiles (24 hours)
   - Cache search results (1 hour)

3. **Query Optimization**
   - Use pagination (default 20 items)
   - Select only needed columns
   - Avoid N+1 queries

## Next Steps

1. Set up PostgreSQL database
2. Create SQLAlchemy models
3. Implement authentication
4. Build article CRUD endpoints
5. Implement search
6. Add email integration
7. Build analytics tracking
8. Calculate trending scores
9. Create admin dashboard
10. Write comprehensive tests
