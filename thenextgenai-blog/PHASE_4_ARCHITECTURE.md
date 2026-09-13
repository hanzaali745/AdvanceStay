# Phase 4: Premium Features & Monetization

## Overview
Phase 4 extends Phase 3 with premium content tiers, subscription management, personalization, and advanced analytics.

## Architecture

### Premium Tier System

#### Tier Levels
```
FREE
├─ Access to public articles
├─ 5,200+ weekly newsletter
├─ Basic author profiles
└─ Limited search (3 searches/day)

PRO ($9/month or $79/year)
├─ All FREE features
├─ Access to 200+ premium research articles
├─ Early access to new articles (24 hours early)
├─ Download articles as PDF
├─ No ads
├─ Email digests (daily/weekly/monthly)
├─ Bookmarks & reading list
├─ Author notifications
└─ Advanced filtering & search

ENTERPRISE (Custom)
├─ All PRO features
├─ Team accounts (up to 10 users)
├─ Custom integrations
├─ Dedicated support
├─ Admin dashboard
└─ Usage analytics API
```

### Database Extensions

#### Subscription Table
```sql
CREATE TABLE subscriptions (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  tier VARCHAR(50) NOT NULL,  -- free, pro, enterprise
  stripe_customer_id VARCHAR(255),
  stripe_subscription_id VARCHAR(255),
  stripe_product_id VARCHAR(255),
  status VARCHAR(50) DEFAULT 'active',  -- active, canceled, past_due, unpaid
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  canceled_at TIMESTAMP,
  trial_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id)
);
```

#### Premium Content Table
```sql
CREATE TABLE premium_articles (
  id SERIAL PRIMARY KEY,
  article_id INT REFERENCES articles(id) ON DELETE CASCADE,
  tier_required VARCHAR(50) NOT NULL,  -- pro, enterprise
  release_date TIMESTAMP,  -- When free users get access
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(article_id)
);
```

#### Email Digest Configuration
```sql
CREATE TABLE email_digest_preferences (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  frequency VARCHAR(50),  -- daily, weekly, monthly
  enabled BOOLEAN DEFAULT TRUE,
  send_time TIME,  -- Preferred send time
  categories JSONB,  -- Selected categories
  authors JSONB,  -- Preferred authors
  last_sent TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id)
);
```

#### User Preferences
```sql
CREATE TABLE user_preferences (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) ON DELETE CASCADE,
  theme VARCHAR(50) DEFAULT 'dark',  -- dark, light, auto
  language VARCHAR(10) DEFAULT 'en',
  timezone VARCHAR(50) DEFAULT 'UTC',
  notifications_enabled BOOLEAN DEFAULT TRUE,
  email_notifications BOOLEAN DEFAULT TRUE,
  marketing_emails BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id)
);
```

### API Endpoints

#### Subscriptions
```
GET    /api/subscriptions/current      # Get user's current subscription
POST   /api/subscriptions/create       # Create new subscription
POST   /api/subscriptions/upgrade      # Upgrade tier
POST   /api/subscriptions/downgrade    # Downgrade tier
POST   /api/subscriptions/cancel       # Cancel subscription
GET    /api/subscriptions/plans        # List available plans
GET    /api/subscriptions/billing-portal # Get Stripe portal link
```

#### Premium Content
```
GET    /api/articles/premium           # List premium articles
GET    /api/articles/{id}/access       # Check article access
GET    /api/articles/{id}/export       # Export article as PDF
POST   /api/articles/{id}/pdf          # Generate PDF
```

#### Email Digests
```
GET    /api/digests/preferences        # Get digest preferences
PUT    /api/digests/preferences        # Update preferences
POST   /api/digests/send-test          # Send test digest
GET    /api/digests/history            # Get digest history
```

#### User Preferences
```
GET    /api/preferences                # Get user preferences
PUT    /api/preferences                # Update preferences
POST   /api/preferences/reset           # Reset to defaults
```

#### Notifications
```
GET    /api/notifications              # List notifications
POST   /api/notifications/subscribe    # Subscribe to author
POST   /api/notifications/unsubscribe  # Unsubscribe from author
GET    /api/notifications/settings     # Get notification settings
PUT    /api/notifications/settings     # Update settings
```

## Stripe Integration

### Setup
```python
# config.py additions
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Pricing
STRIPE_PLANS = {
    "pro_monthly": "price_xxx",
    "pro_annual": "price_yyy",
    "enterprise": "price_zzz"
}
```

### Subscription Flow
```
1. User clicks "Upgrade to Pro"
2. Frontend: Redirect to Stripe Checkout
3. Stripe: User enters payment info
4. Stripe: Calls webhook on success
5. Backend: Create subscription in DB
6. Backend: Update user tier to PRO
7. Frontend: Confirm upgrade success
```

### Webhook Handlers
```python
# Stripe Events to Handle:
- customer.subscription.created
- customer.subscription.updated
- customer.subscription.deleted
- invoice.payment_succeeded
- invoice.payment_failed
- charge.refunded
```

### Code Example
```python
from stripe import stripe

# Create checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': STRIPE_PLANS['pro_monthly'],
        'quantity': 1,
    }],
    customer_email=user.email,
    mode='subscription',
    success_url=f"{FRONTEND_URL}/subscription/success?session_id={{CHECKOUT_SESSION_ID}}",
    cancel_url=f"{FRONTEND_URL}/subscription/canceled",
)

# Handle webhook
@app.post("/api/webhooks/stripe")
def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event['type'] == 'customer.subscription.created':
        handle_subscription_created(event['data']['object'])
    
    return {"status": "received"}
```

## Email Digest System

### Digest Generation
```python
class DigestService:
    @staticmethod
    def generate_digest(user_id: int, db: Session) -> str:
        user = db.query(User).get(user_id)
        prefs = user.digest_preferences
        
        # Get articles matching preferences
        articles = db.query(Article).filter(
            Article.is_published == True,
            Article.category.in_(prefs.categories),
            Article.author_id.in_(prefs.authors)
        ).order_by(Article.created_at.desc()).limit(10).all()
        
        # Render HTML template
        html = render_digest_template(articles, user)
        return html
    
    @staticmethod
    def schedule_digests(db: Session):
        # Find users with digests due
        users = db.query(User).join(EmailDigestPreferences).filter(
            EmailDigestPreferences.enabled == True,
            # ... time-based filter
        ).all()
        
        for user in users:
            digest_html = DigestService.generate_digest(user.id, db)
            email_service.send_email(user.email, digest_html)
            # Update last_sent
```

### Digest Templates
```html
<!-- templates/digest_weekly.html -->
<h1>The Next Gen AI - Weekly Digest</h1>
<p>{{ week_range }}</p>

{% for article in articles %}
  <div class="article">
    <h2>{{ article.title }}</h2>
    <p>By {{ article.author.name }}</p>
    <p>{{ article.excerpt }}</p>
    <a href="{{ frontend_url }}/articles/{{ article.slug }}">Read Article</a>
  </div>
{% endfor %}

<p><a href="{{ frontend_url }}/preferences">Manage Preferences</a></p>
```

### Scheduled Jobs (Celery/APScheduler)
```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=9, minute=0)
def send_daily_digests():
    DigestService.send_daily_digests()

@scheduler.scheduled_job('cron', day_of_week='mon', hour=9, minute=0)
def send_weekly_digests():
    DigestService.send_weekly_digests()

@scheduler.scheduled_job('cron', day=1, hour=9, minute=0)
def send_monthly_digests():
    DigestService.send_monthly_digests()

scheduler.start()
```

## Personalization Engine

### User Profile Building
```python
class PersonalizationService:
    @staticmethod
    def track_user_interests(user_id: int, db: Session):
        """Build interest profile from reading history"""
        reading_history = db.query(ReadingHistory).filter(
            ReadingHistory.user_id == user_id
        ).all()
        
        # Calculate category preferences
        category_weights = {}
        for read in reading_history:
            article = read.article
            category = article.category
            category_weights[category] = category_weights.get(category, 0) + 1
        
        # Calculate author preferences
        author_weights = {}
        for read in reading_history:
            article = read.article
            author_id = article.author_id
            author_weights[author_id] = author_weights.get(author_id, 0) + 1
        
        return {
            "categories": category_weights,
            "authors": author_weights
        }
    
    @staticmethod
    def get_recommendations(user_id: int, db: Session, limit: int = 10):
        """Generate personalized article recommendations"""
        interests = PersonalizationService.track_user_interests(user_id, db)
        
        # Find unread articles matching preferences
        recommended = db.query(Article).filter(
            Article.id.notin_(
                db.query(ReadingHistory.article_id).filter(
                    ReadingHistory.user_id == user_id
                )
            ),
            Article.is_published == True,
            Article.category.in_(interests['categories'].keys())
        ).order_by(Article.created_at.desc()).limit(limit).all()
        
        return recommended
```

## Analytics Dashboard (Admin)

### Admin Endpoints
```
GET    /api/admin/analytics/overview         # Overview stats
GET    /api/admin/analytics/articles         # Article performance
GET    /api/admin/analytics/users            # User analytics
GET    /api/admin/analytics/revenue          # Subscription revenue
GET    /api/admin/analytics/engagement       # Engagement metrics
GET    /api/admin/analytics/content          # Content performance
```

### Metrics Tracked
```
- Daily/Monthly active users
- Subscription churn rate
- MRR (Monthly Recurring Revenue)
- LTV (Customer Lifetime Value)
- Reading time metrics
- Content performance
- Author statistics
- Trending analysis
- Search analytics
```

## Frontend Integration

### React Components Needed
```
- SubscriptionCard (tier selection)
- UpgradeModal
- StripeCheckout (via Stripe.js)
- BillingPortal (customer portal)
- DigestPreferences
- NotificationSettings
- UserPreferences
- RecommendationPanel
- PremiumBadge (content indicator)
```

### Auth Flow Updates
```javascript
// Check subscription on login
const user = await getUser()
if (user.tier === 'free') {
  show_upgrade_prompt()
}

// Check article access
const canRead = await checkArticleAccess(articleId)
if (!canRead) {
  show_upgrade_modal()
}
```

## Infrastructure

### Services
- **Stripe**: Payment processing & subscriptions
- **SendGrid**: Email delivery
- **APScheduler/Celery**: Background jobs for digests
- **Redis**: Caching & session management (optional)

### Monitoring
- Stripe webhook failures
- Email delivery failures
- Subscription sync issues
- Analytics calculation delays

## Security Considerations

1. **Webhook Verification**: Always verify Stripe webhook signatures
2. **Payment Data**: Never store credit card details (Stripe handles this)
3. **Subscription Verification**: Always check subscription status server-side before granting access
4. **Rate Limiting**: Limit API requests per tier
5. **Data Privacy**: Encrypt sensitive user data, follow GDPR/CCPA

## Deployment Checklist

- [ ] Set up Stripe account & API keys
- [ ] Configure SendGrid API key
- [ ] Set up environment variables
- [ ] Database migration for new tables
- [ ] Schedule APScheduler jobs
- [ ] Deploy webhook endpoint (publicly accessible)
- [ ] Test Stripe integration (test mode first)
- [ ] Set up monitoring/alerts
- [ ] Configure email templates
- [ ] Test subscription flow end-to-end
