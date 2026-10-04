import json
import urllib.error
from unittest.mock import MagicMock, patch

import pytest

from decider.jev_client import JevClient


@pytest.fixture
def jev_client():
    return JevClient(api_key="test_key", base_url="https://api.test")


def test_post_decision_success(jev_client):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(
        {"code": 0, "message": "ok", "data": {"decision": "test_decision"}}
    ).encode("utf-8")
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        result = jev_client.post_decision("/test", {"payload": "test"})

        assert result["code"] == 0
        assert result["data"]["decision"] == "test_decision"


def test_post_decision_api_error(jev_client):
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"code": 1, "message": "Invalid request"}).encode(
        "utf-8"
    )
    mock_response.__enter__.return_value = mock_response

    with patch("urllib.request.urlopen", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Jev API error: Invalid request"):
            jev_client.post_decision("/test", {"payload": "test"})


def test_post_decision_http_error(jev_client):
    error = urllib.error.HTTPError(
        url="https://api.test/test", code=401, msg="Unauthorized", hdrs=None, fp=None
    )
    # Mock read for the HTTPError body
    error.read = MagicMock(return_value=json.dumps({"message": "Invalid API key"}).encode("utf-8"))

    with patch("urllib.request.urlopen", side_effect=error):
        with pytest.raises(RuntimeError, match="Jev API HTTP 401: Invalid API key"):
            jev_client.post_decision("/test", {"payload": "test"})


def test_post_decision_url_error(jev_client):
    error = urllib.error.URLError("Connection refused")

    with patch("urllib.request.urlopen", side_effect=error):
        with pytest.raises(RuntimeError, match="Jev API connection error"):
            jev_client.post_decision("/test", {"payload": "test"})
