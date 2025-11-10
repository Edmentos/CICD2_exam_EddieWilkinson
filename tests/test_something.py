import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.models import Base

TEST_DB_URL = "sqlite:///memory:"
engine = create_engine(
    TEST_DB_URL,
    connect_args - {"chekc_same_thread":False}
    poolclass = StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine,expire_on_commit=False,autoflush = False)

@pytest.fixture(scope = "function")
def client():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)

    def override_get_db():
        db=TestingSessionLocal()
        try:
            yield db
        finally:
            db.close

app.dependency_overrides[get_db] = override_get_db

with TestClient(app) as c:
    yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)

def test_create_author(client):
    r = client.post("api/authors", json = {"id": 1, "name": "Eddie", "email": "Eddie@atu.ie", "year_started": 2000})
    assert r.status_code == 201

