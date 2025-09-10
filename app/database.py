from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

if not settings.DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Provide it via environment variable or .env file.")

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
