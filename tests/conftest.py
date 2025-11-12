import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.dependencies.database import get_db
from app.main import app
import os

# Подключаем тестовую БД
DATABASE_TEST_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5433/qadb_test")
engine = create_engine(DATABASE_TEST_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц перед тестами
Base.metadata.create_all(bind=engine)

# Фикстура сессии БД
@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Фикстура TestClient
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
