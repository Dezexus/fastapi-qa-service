import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.dependencies.database import get_db
from app.main import app
from app.core.logger import get_logger

logger = get_logger("tests")

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL", "postgresql://postgres:postgres@localhost:5433/qadb_test")

engine = create_engine(DATABASE_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    logger.debug("Setting up test database")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    logger.debug("Test database teardown completed")

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    logger.debug("Test client setup completed")
    yield TestClient(app)
    app.dependency_overrides.clear()
    logger.debug("Test client teardown completed")