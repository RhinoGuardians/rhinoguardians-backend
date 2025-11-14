"""Test configuration for pytest"""
import os
import sys
import types
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure project root importable
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Keep YOLO lightweight during tests
os.environ.setdefault("SKIP_YOLO", "1")

from main import app  # noqa: E402
from database.db import get_db  # noqa: E402
from database.models import Base  # noqa: E402

# Isolated in-memory DB for tests
TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override app's DB dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def mock_notifications(monkeypatch):
    """Patch notifications to avoid external side effects."""
    import routes.alerts as alerts_module

    async def fake_send_alert(self=None, **kwargs) -> bool:
        return True

    if hasattr(alerts_module, "notification_service"):
        monkeypatch.setattr(
            alerts_module.notification_service,
            "send_alert",
            types.MethodType(fake_send_alert, alerts_module.notification_service),
            raising=True,
        )
    else:
        import utils.notifications as notifications_module
        monkeypatch.setattr(
            notifications_module.NotificationService,
            "send_alert",
            fake_send_alert,
            raising=True,
        )
    yield

@pytest.fixture()
def client():
    return TestClient(app)
