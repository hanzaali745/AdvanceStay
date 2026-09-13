from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import logging
from database.models import Article, AnalyticsEvent, ReadingHistory
from config import settings

logger = logging.getLogger(__name__)

class TrendingService:
    """Service for calculating and managing trending articles"""

    @staticmethod
    def calculate_trending_score(article: Article, db: Session) -> float:
        """
        Calculate a trending score for an article (0-100)

        Formula:
        Score = (0.3 * View Count) +
                (0.25 * Read Completion %) +
                (0.2 * Engagement Score) +
                (0.15 * Recency Factor) +
                (0.1 * Author Reputation)
        """

        # 1. View count factor (0.3 weight)
        view_count = article.view_count
        max_views = 1000
        view_score = min((view_count / max_views) * 100, 100) * 0.3

        # 2. Read completion factor (0.25 weight)
        completion_rate = TrendingService._get_completion_rate(article.id, db)
        read_score = completion_rate * 0.25

        # 3. Engagement factor (0.2 weight)
        engagement_score = TrendingService._get_engagement_score(article.id, db)
        engagement_factor = engagement_score * 0.2

        # 4. Recency factor (0.15 weight)
        recency_score = TrendingService._get_recency_score(article.created_at)
        recency_factor = recency_score * 0.15

        # 5. Author reputation (0.1 weight)
        author_score = TrendingService._get_author_reputation(article.author, db)
        author_factor = author_score * 0.1

        total_score = view_score + read_score + engagement_factor + recency_factor + author_factor
        return min(total_score, 100)

    @staticmethod
    def _get_completion_rate(article_id: int, db: Session) -> float:
        """Calculate percentage of readers who completed the article"""
        completed = db.query(func.count(ReadingHistory.id)).filter(
            ReadingHistory.article_id == article_id,
            ReadingHistory.completed == True
        ).scalar() or 0

        total = db.query(func.count(ReadingHistory.id)).filter(
            ReadingHistory.article_id == article_id
        ).scalar() or 1

        return (completed / total * 100) if total > 0 else 0

    @staticmethod
    def _get_engagement_score(article_id: int, db: Session) -> float:
        """Calculate engagement based on bookmarks and interactions"""
        engagement_count = db.query(func.count(AnalyticsEvent.id)).filter(
            AnalyticsEvent.article_id == article_id,
            AnalyticsEvent.event_type.in_(["bookmark", "share", "comment"])
        ).scalar() or 0

        max_engagement = 50
        return min((engagement_count / max_engagement) * 100, 100)

    @staticmethod
    def _get_recency_score(created_at: datetime) -> float:
        """Calculate recency score (newer articles score higher)"""
        days_old = (datetime.utcnow() - created_at).days
        date_range = settings.trending_date_range_days

        if days_old <= 0:
            return 100
        elif days_old >= date_range:
            return 0
        else:
            return ((date_range - days_old) / date_range) * 100

    @staticmethod
    def _get_author_reputation(author, db: Session) -> float:
        """Calculate author reputation based on historical performance"""
        if not author:
            return 50

        if author.verification_status == "expert":
            return 100
        elif author.verification_status == "verified":
            return 80
        else:
            # Calculate based on average article performance
            avg_views = db.query(func.avg(Article.view_count)).filter(
                Article.author_id == author.id
            ).scalar() or 0

            avg_score = min((avg_views / 500) * 100, 100)
            return avg_score

    @staticmethod
    def recalculate_all_trending(db: Session) -> int:
        """Recalculate trending scores for all articles"""
        try:
            # Only rank articles published > 24 hours ago with > min_views
            cutoff_time = datetime.utcnow() - timedelta(hours=24)

            articles = db.query(Article).filter(
                Article.is_published == True,
                Article.created_at < cutoff_time,
                Article.view_count >= settings.trending_min_views
            ).all()

            # Calculate scores and assign ranks
            scores = []
            for article in articles:
                score = TrendingService.calculate_trending_score(article, db)
                scores.append((article.id, score))

            # Sort by score descending and assign ranks
            scores.sort(key=lambda x: x[1], reverse=True)

            for rank, (article_id, score) in enumerate(scores, 1):
                article = db.query(Article).get(article_id)
                article.trending_rank = rank
                article.confidence_score = int(score)

            db.commit()
            logger.info(f"Recalculated trending for {len(articles)} articles")
            return len(articles)

        except Exception as e:
            logger.error(f"Error recalculating trending: {str(e)}")
            db.rollback()
            return 0

    @staticmethod
    def get_trending_articles(db: Session, limit: int = 10) -> list:
        """Get top trending articles"""
        return db.query(Article).filter(
            Article.is_published == True,
            Article.trending_rank.isnot(None)
        ).order_by(Article.trending_rank.asc()).limit(limit).all()

# Singleton instance
trending_service = TrendingService()
