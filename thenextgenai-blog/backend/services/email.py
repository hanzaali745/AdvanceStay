import logging
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Email service abstraction supporting multiple providers"""

    @staticmethod
    def send_welcome_email(email: str, name: str) -> bool:
        """Send welcome email to new subscriber"""
        subject = "Welcome to The Next Gen AI"
        body = f"""
        <h1>Welcome {name}!</h1>
        <p>Thank you for subscribing to The Next Gen AI newsletter.</p>
        <p>Every Tuesday, we send verified insights on:</p>
        <ul>
            <li>LLMs and transformer architecture</li>
            <li>Prompt engineering techniques</li>
            <li>Cutting-edge AI research</li>
            <li>Practical AI applications</li>
        </ul>
        <p>Curated by domain experts. Fact-checked. Updated weekly.</p>
        <p>Unsubscribe anytime.</p>
        """
        return EmailService._send_email(email, subject, body)

    @staticmethod
    def send_password_reset_email(email: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"
        subject = "Reset Your Password"
        body = f"""
        <h1>Reset Your Password</h1>
        <p>Click the link below to reset your password:</p>
        <a href="{reset_url}">Reset Password</a>
        <p>Link expires in 1 hour.</p>
        <p>If you didn't request this, ignore this email.</p>
        """
        return EmailService._send_email(email, subject, body)

    @staticmethod
    def send_article_published_email(email: str, article_title: str, article_slug: str) -> bool:
        """Notify subscribers of new article"""
        article_url = f"{settings.frontend_url}/article/{article_slug}"
        subject = f"New Article: {article_title}"
        body = f"""
        <h1>New Article Published</h1>
        <h2>{article_title}</h2>
        <p><a href="{article_url}">Read Article</a></p>
        """
        return EmailService._send_email(email, subject, body)

    @staticmethod
    def send_weekly_digest(email: str, articles: list) -> bool:
        """Send weekly newsletter digest"""
        articles_html = "".join([
            f"""
            <div style="margin: 20px 0; padding: 15px; border: 1px solid #e0e0e0;">
                <h3>{article['title']}</h3>
                <p>{article['excerpt']}</p>
                <a href="{settings.frontend_url}/article/{article['slug']}">Read Article</a>
            </div>
            """
            for article in articles
        ])

        subject = "The Next Gen AI - Weekly Digest"
        body = f"""
        <h1>The Next Gen AI - Weekly Digest</h1>
        <p>Your curated selection of this week's top articles:</p>
        {articles_html}
        <p><a href="{settings.frontend_url}/unsubscribe">Unsubscribe</a></p>
        """
        return EmailService._send_email(email, subject, body)

    @staticmethod
    def _send_email(to_email: str, subject: str, body: str) -> bool:
        """Internal method to send email via provider"""
        if not settings.sendgrid_api_key:
            logger.warning("Email service not configured (no API key)")
            return False

        try:
            if settings.email_provider == "sendgrid":
                return EmailService._send_via_sendgrid(to_email, subject, body)
            else:
                logger.error(f"Unknown email provider: {settings.email_provider}")
                return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    def _send_via_sendgrid(to_email: str, subject: str, body: str) -> bool:
        """Send email via SendGrid"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            message = Mail(
                from_email=settings.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=body
            )

            sg = SendGridAPIClient(settings.sendgrid_api_key)
            response = sg.send(message)
            return response.status_code in [200, 201, 202]
        except Exception as e:
            logger.error(f"SendGrid error: {str(e)}")
            return False

# Singleton instance
email_service = EmailService()
