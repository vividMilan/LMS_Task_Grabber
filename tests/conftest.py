import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database.models import Base


@pytest.fixture(scope='function')
def db() -> Session:
    """Creates a fresh, isolated in-memory database session for each test function."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    # Create all tables in memory
    Base.metadata.create_all(bind=engine)

    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)