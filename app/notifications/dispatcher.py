"""
Notification delivery. The dashboard channel is always available (it is
just the `alerts` table, already written by the caller before this runs).
Email/Telegram/Discord/push are integration points: wire real sending
code in behind each `_send_*` function once credentials are configured
in .env — do not fake a successful delivery in the meantime.
"""
from dataclasses import dataclass

from app.database.models.enums import AlertChannel
from app.settings.config import Settings


@dataclass
class DeliveryResult:
    delivered: bool
    error: str | None = None


def _send_email(settings: Settings, title: str, message: str) -> DeliveryResult:
    if not settings.smtp_host:
        return DeliveryResult(delivered=False, error="Waiting for SMTP configuration (SMTP_HOST not set)")
    # INTEGRATION POINT: send via smtplib/SES/etc. once SMTP_HOST/USER/PASSWORD are configured.
    raise NotImplementedError("Email delivery is not yet implemented — SMTP credentials are configured but unused")


def _send_telegram(settings: Settings, title: str, message: str) -> DeliveryResult:
    if not settings.telegram_bot_token:
        return DeliveryResult(delivered=False, error="Waiting for Telegram bot token (TELEGRAM_BOT_TOKEN not set)")
    # INTEGRATION POINT: call the Telegram Bot API sendMessage endpoint here.
    raise NotImplementedError("Telegram delivery is not yet implemented")


def _send_discord(settings: Settings, title: str, message: str) -> DeliveryResult:
    if not settings.discord_webhook_url:
        return DeliveryResult(delivered=False, error="Waiting for Discord webhook URL (DISCORD_WEBHOOK_URL not set)")
    # INTEGRATION POINT: POST to the Discord webhook URL here.
    raise NotImplementedError("Discord delivery is not yet implemented")


def _send_push(settings: Settings, title: str, message: str) -> DeliveryResult:
    # INTEGRATION POINT: no push provider (e.g. FCM/APNs/web-push) is wired up yet.
    return DeliveryResult(delivered=False, error="Waiting for push notification provider integration")


def send_notification(settings: Settings, *, channel: AlertChannel, title: str, message: str) -> DeliveryResult:
    if channel == AlertChannel.DASHBOARD:
        return DeliveryResult(delivered=True)
    if channel == AlertChannel.EMAIL:
        return _send_email(settings, title, message)
    if channel == AlertChannel.TELEGRAM:
        return _send_telegram(settings, title, message)
    if channel == AlertChannel.DISCORD:
        return _send_discord(settings, title, message)
    if channel == AlertChannel.PUSH:
        return _send_push(settings, title, message)
    return DeliveryResult(delivered=False, error=f"Unknown channel: {channel}")
