from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.dependencies import get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a TestClient for the FastAPI app."""

    test_engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        bind=test_engine, autocommit=False, autoflush=False
    )

    # Create the database tables
    Base.metadata.create_all(bind=test_engine)

    # override the get_db dependency
    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        # cleanup dependencies, drop tables, and dispose of the engine
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()
