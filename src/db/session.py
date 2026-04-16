from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup
DB_NAME = "assignments.db"
SQLALCHEMY_DATABASE_URL = f'sqlite:///{DB_NAME}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from contextlib import contextmanager


def init_db():
    from .models import Base
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()