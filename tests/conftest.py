import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import get_db
from app.main import app

load_dotenv('.env.test')

raw_test_db_url = os.getenv('TEST_DATABASE_URL')
if not raw_test_db_url:
    raise RuntimeError('TEST_DATABASE_URL is not set. Define it in .env.test')

if 'test' not in raw_test_db_url:
    raise RuntimeError('Unsafe TEST_DATABASE_URL. Expected a dedicated test database URL.')

TEST_DATABASE_URL: str = raw_test_db_url


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(bind=connection, autocommit=False, autoflush=False)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
