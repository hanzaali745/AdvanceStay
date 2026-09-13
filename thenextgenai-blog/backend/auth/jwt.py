from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from config import settings

def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiration_hours)

    to_encode = {"sub": str(user_id), "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt

def create_refresh_token(user_id: int) -> str:
    """Create a JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expiration_days)
    to_encode = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[int]:
    """Extract user_id from a JWT token"""
    payload = decode_token(token)
    if payload is None:
        return None
    try:
        user_id = int(payload.get("sub"))
        return user_id
    except (TypeError, ValueError):
        return None
