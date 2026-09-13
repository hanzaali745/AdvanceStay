# The Next Gen AI - Backend API

FastAPI-based backend for The Next Gen AI blog platform.

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- pip or poetry

### Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Create PostgreSQL database:**
   ```bash
   createdb thenextgenai
   ```

5. **Initialize database and seed data:**
   ```bash
   python -c "
   from app import engine, SessionLocal
   from database.models import Base
   from database.seed import seed_database
   
   Base.metadata.create_all(bind=engine)
   db = SessionLocal()
   seed_database(db)
   "
   ```

## Running

### Development server
```bash
python app.py
# or
uvicorn app:app --reload
```

Server runs on http://localhost:8000

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/profile` - Update profile
- `POST /api/auth/refresh` - Refresh token

### Articles
- `GET /api/articles` - List articles (paginated)
- `GET /api/articles/{id}` - Get article by ID
- `GET /api/articles/slug/{slug}` - Get article by slug
- `POST /api/articles` - Create article (admin)
- `PUT /api/articles/{id}` - Update article (admin)
- `DELETE /api/articles/{id}` - Delete article (admin)
- `GET /api/articles/category/{category}` - Articles by category
- `POST /api/articles/{id}/view` - Track view
- `POST /api/articles/{id}/read` - Track read

### Authors
- `GET /api/authors` - List all authors
- `GET /api/authors/{id}` - Get author by ID
- `GET /api/authors/slug/{slug}` - Get author by slug
- `POST /api/authors` - Create author (admin)
- `GET /api/authors/{id}/articles` - Get author's articles

### Search
- `GET /api/search` - Full-text search
- `GET /api/search/suggestions` - Search suggestions
- `GET /api/search/trending-queries` - Trending searches

### Newsletter
- `POST /api/newsletter/subscribe` - Subscribe
- `POST /api/newsletter/unsubscribe` - Unsubscribe
- `POST /api/newsletter/verify` - Verify email
- `GET /api/newsletter/status` - Subscription status
- `GET /api/newsletter` - List subscribers (admin)
- `GET /api/newsletter/stats` - Newsletter stats

### Trending
- `GET /api/trending` - Get trending articles
- `POST /api/trending/recalculate` - Recalculate scores (admin)
- `GET /api/trending/top` - Top articles from past N days
- `GET /api/trending/by-category/{category}` - Trending by category
- `GET /api/trending/score/{id}` - Get article score breakdown

### Analytics
- `POST /api/analytics/event` - Track event
- `GET /api/analytics/user/{id}` - User analytics
- `GET /api/analytics/articles` - Article analytics
- `GET /api/analytics/overview` - Overview stats
- `GET /api/analytics/events` - List events

## Database Schema

### Tables
- `users` - User accounts and profiles
- `authors` - Expert contributors
- `articles` - Blog articles and content
- `newsletter_subscribers` - Email subscribers
- `bookmarks` - User saved articles
- `reading_history` - User reading progress
- `analytics_events` - User behavior tracking

## Authentication

All protected endpoints require JWT token in Authorization header:

```
Authorization: Bearer <access_token>
```

Tokens expire in 24 hours. Use `/api/auth/refresh` to get new token.

## Testing

Sample requests:

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# List articles
curl http://localhost:8000/api/articles

# Search
curl "http://localhost:8000/api/search?q=llm&page=1"

# Get trending
curl http://localhost:8000/api/trending

# Subscribe
curl -X POST http://localhost:8000/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "User"}'
```

## Environment Variables

See `.env.example` for all available options.

**Important security:**
- Change `SECRET_KEY` and `JWT_SECRET` in production
- Use strong database password
- Set `ENVIRONMENT=production` in production
- Use HTTPS for all endpoints
- Configure proper CORS origins

## Architecture

```
app.py                      # FastAPI application
├── config.py              # Configuration
├── database/
│   ├── models.py          # SQLAlchemy ORM models
│   └── schemas.py         # Pydantic schemas
├── api/
│   ├── auth.py            # Authentication endpoints
│   ├── articles.py        # Article CRUD
│   ├── authors.py         # Author management
│   ├── search.py          # Search functionality
│   ├── newsletter.py      # Newsletter management
│   ├── trending.py        # Trending calculations
│   └── analytics.py       # Analytics tracking
├── auth/
│   ├── jwt.py             # JWT token handling
│   └── password.py        # Password hashing
└── services/
    ├── email.py           # Email service
    └── trending.py        # Trending algorithm
```

## Deployment

See `/PHASE_3_ARCHITECTURE.md` for Docker setup and deployment instructions.

## Development

### Add new endpoint
1. Create router in `/api/`
2. Add router to `app.py`
3. Test with `/docs`
4. Document in README

### Modify database
1. Update models in `database/models.py`
2. Create migration with Alembic
3. Update schemas in `database/schemas.py`

## Support

For issues or questions, see project documentation in root directory.
