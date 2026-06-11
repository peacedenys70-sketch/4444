import os
from dotenv import load_dotenv
from pathlib import Path

# Charger .env en local (ignoré sur Render car les vars sont définies dans le dashboard)
load_dotenv(dotenv_path=Path(__file__).parent / '.env')


class Config:
    # Base de données — Render injecte DATABASE_URL automatiquement
    _db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/mentorlink')
    # Render fournit parfois "postgres://" (ancien format) → corriger en "postgresql://"
    if _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI      = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY           = os.getenv('JWT_SECRET_KEY', 'change-me-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    DEBUG                    = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    MAX_CONTENT_LENGTH       = 5 * 1024 * 1024   # 5 Mo max (photos base64)
