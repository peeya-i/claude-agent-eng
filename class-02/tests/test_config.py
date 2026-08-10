from class_02.config import load_config


def test_load_config_returns_defaults(monkeypatch):
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)

    config = load_config()

    assert config.name
    assert config.log_level
    assert config.model


def test_load_config_env_override(monkeypatch):
    monkeypatch.setenv("APP_NAME", "overridden")

    config = load_config()

    assert config.name == "overridden"
