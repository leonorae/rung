import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from rung.main import app
from rung.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        'sqlite://', # in memory instead of file
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    get_session()

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override # type: ignore
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()