from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from database.models import NewsletterSubscriber
from database.schemas import NewsletterSubscribeRequest, NewsletterSubscriberResponse
from services.email import email_service

router = APIRouter(prefix="/api/newsletter", tags=["newsletter"])

def get_db():
    from app import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subscribe", response_model=dict, status_code=201)
def subscribe_newsletter(
    request: NewsletterSubscribeRequest,
    db: Session = Depends(get_db)
):
    """Subscribe to newsletter"""
    existing = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == request.email
    ).first()

    if existing:
        if existing.is_active:
            raise HTTPException(
                status_code=400,
                detail="Already subscribed to newsletter"
            )
        else:
            # Resubscribe
            existing.is_active = True
            existing.subscribed_at = datetime.utcnow()
            existing.unsubscribed_at = None
            existing.frequency = request.frequency
            db.commit()
            return {"message": "Resubscribed successfully"}

    verification_token = secrets.token_urlsafe(32)

    subscriber = NewsletterSubscriber(
        email=request.email,
        name=request.name,
        frequency=request.frequency,
        verification_token=verification_token,
        is_verified=False,
        is_active=True
    )

    db.add(subscriber)
    db.commit()
    db.refresh(subscriber)

    # Send welcome email
    email_service.send_welcome_email(request.email, request.name or "Subscriber")

    return {
        "message": "Subscribed successfully. Check email for verification.",
        "email": request.email
    }

@router.post("/unsubscribe")
def unsubscribe_newsletter(
    email: str,
    db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    subscriber = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == email
    ).first()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")

    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.utcnow()
    db.commit()

    return {"message": "Unsubscribed successfully"}

@router.post("/verify")
def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify email address"""
    subscriber = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.verification_token == token
    ).first()

    if not subscriber:
        raise HTTPException(status_code=404, detail="Invalid verification token")

    subscriber.is_verified = True
    db.commit()

    return {"message": "Email verified successfully"}

@router.get("/status")
def subscription_status(
    email: str,
    db: Session = Depends(get_db)
):
    """Check subscription status"""
    subscriber = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.email == email
    ).first()

    if not subscriber:
        return {"subscribed": False}

    return {
        "subscribed": subscriber.is_active,
        "verified": subscriber.is_verified,
        "frequency": subscriber.frequency,
        "subscribed_at": subscriber.subscribed_at
    }

@router.get("", response_model=dict)
def list_subscribers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20),
    db: Session = Depends(get_db)
):
    """List all active subscribers (admin only)"""
    query = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.is_active == True
    )

    total = query.count()
    subscribers = query.offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "subscribers": [NewsletterSubscriberResponse.from_orm(s) for s in subscribers]
    }

@router.get("/stats")
def newsletter_stats(db: Session = Depends(get_db)):
    """Get newsletter statistics"""
    total_subscribers = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.is_active == True
    ).count()

    verified_subscribers = db.query(NewsletterSubscriber).filter(
        (NewsletterSubscriber.is_active == True) &
        (NewsletterSubscriber.is_verified == True)
    ).count()

    daily = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.frequency == "daily"
    ).count()

    weekly = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.frequency == "weekly"
    ).count()

    monthly = db.query(NewsletterSubscriber).filter(
        NewsletterSubscriber.frequency == "monthly"
    ).count()

    return {
        "total": total_subscribers,
        "verified": verified_subscribers,
        "by_frequency": {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly
        }
    }
