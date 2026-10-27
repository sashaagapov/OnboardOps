import pytest
from fastapi.testclient import TestClient
from database import init_db


@pytest.fixture
def initialized_database(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_db()
    return tmp_path


@pytest.fixture
def api_client(initialized_database):
    from api import app

    with TestClient(app) as client:
        yield client