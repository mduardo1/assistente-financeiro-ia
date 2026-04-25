from pathlib import Path
import uuid

import pytest

from app import create_app
from app.config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture()
def app():
    workspace_temp_dir = Path.cwd() / ".tmp_test_runs"
    workspace_temp_dir.mkdir(exist_ok=True)
    database_path = workspace_temp_dir / f"test_{uuid.uuid4().hex}.db"

    LocalTestConfig = type(
        "LocalTestConfig",
        (TestConfig,),
        {
            "DATABASE_PATH": database_path,
            "SECRET_KEY": "test-secret",
        },
    )

    flask_app = create_app(LocalTestConfig)
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()
