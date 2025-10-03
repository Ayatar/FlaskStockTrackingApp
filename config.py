import os
from dotenv import load_dotenv

load_dotenv()


def _get_bool_env(name: str, default: bool = False) -> bool:
    """Return boolean environment variables in a safe way."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {'1', 'true', 't', 'yes', 'y'}


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///stok.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookie security settings (configurable via environment variables)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _get_bool_env('SESSION_COOKIE_SECURE', False)
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = _get_bool_env('REMEMBER_COOKIE_SECURE', False)

    # CSRF configuration
    WTF_CSRF_TIME_LIMIT = int(os.getenv('WTF_CSRF_TIME_LIMIT', 3600))