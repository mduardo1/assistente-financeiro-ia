from pathlib import Path
import tempfile

import pytest

from app import create_app
from app.config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture()
def app():
    temp_dir = tempfile.TemporaryDirectory()
    database_path = Path(temp_dir.name) / "test.db"

    class LocalTestConfig(TestConfig):
        DATABASE_PATH = database_path
        SECRET_KEY = "test-secret"

    flask_app = create_app(LocalTestConfig)
    yield flask_app
    temp_dir.cleanup()


@pytest.fixture()
def client(app):
    return app.test_client()
