
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from src.config.config import Config

from src.DB.model import User, UrlMapper

engine = create_engine(
    Config.DATABASE_URL, 
    echo=False,  # Disable SQL query logging for production performance
    pool_pre_ping=True,  # Check connections before using them
    pool_size=10,  # Connection pool size
    max_overflow=20  # Max overflow connections
)


def init_db():
        SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

init_db()
