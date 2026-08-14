from pathlib import Path
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base


project_root = Path(__file__).parent.parent.parent
data_dir = project_root / "data"
data_dir.mkdir(exist_ok=True)

DB_PATH = data_dir / "app.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def init_db() -> None:
    """Creates all tables defined in models (Course, File, Assignment) if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_session() -> Session:
    """Provides a database session instance."""
    return SessionLocal()

def reset_database(db_engine: Engine = engine) -> None:
    """Drops all tables and recreates them fresh.

    Ideal for setup/teardown between test runs or local resets.
    """
    Base.metadata.drop_all(bind=db_engine)
    Base.metadata.create_all(bind=db_engine)


