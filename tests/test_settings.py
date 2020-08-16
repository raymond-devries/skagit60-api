from app.settings import get_env


def test_get_env_no_env(monkeypatch):
    assert get_env("DB_SERVER", "localhost") == "localhost"


def test_get_env_with_env(monkeypatch):
    monkeypatch.setenv("DB_SERVER", "test_server")
    assert get_env("DB_SERVER", "localhost") == "test_server"
