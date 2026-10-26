import runpy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


PROJECT_ROOT = Path(__file__).parent


@pytest.fixture
def initialized_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(PROJECT_ROOT / "database.py"))
    return tmp_path


@pytest.fixture
def api_client(initialized_database):
    from api import app

    return TestClient(app)
