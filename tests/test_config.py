from decider.config import Settings, load_settings


def test_default_settings(monkeypatch):
    monkeypatch.delenv("DECIDER_MODE", raising=False)
    monkeypatch.delenv("JEV_API_KEY", raising=False)
    monkeypatch.delenv("JEV_API_BASE_URL", raising=False)
    monkeypatch.delenv("DECISION_CONFIDENCE_THRESHOLD", raising=False)

    settings = load_settings()
    assert settings.decider_mode == "mock"
    assert settings.jev_api_key == ""
    assert settings.jev_api_base_url == "https://www.jevai.org"
    assert settings.decision_confidence_threshold == 0.80


def test_custom_settings(monkeypatch):
    monkeypatch.setenv("DECIDER_MODE", "live")
    monkeypatch.setenv("JEV_API_KEY", "supersecret")
    monkeypatch.setenv("JEV_API_BASE_URL", "https://api.test.com")
    monkeypatch.setenv("DECISION_CONFIDENCE_THRESHOLD", "0.95")

    settings = load_settings()
    assert settings.decider_mode == "live"
    assert settings.jev_api_key == "supersecret"
    assert settings.jev_api_base_url == "https://api.test.com"
    assert settings.decision_confidence_threshold == 0.95

    diag = settings.diagnostics()
    assert diag["jev_api_key"] == "configured"
    assert "supersecret" not in diag.values()


def test_invalid_threshold(monkeypatch):
    monkeypatch.setenv("DECISION_CONFIDENCE_THRESHOLD", "invalid_float")
    settings = load_settings()
    assert settings.decision_confidence_threshold == 0.80


def test_empty_api_key_diagnostics():
    settings = Settings(jev_api_key="")
    diag = settings.diagnostics()
    assert diag["jev_api_key"] == "not configured"
