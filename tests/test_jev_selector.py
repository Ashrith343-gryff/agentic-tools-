from unittest.mock import MagicMock

import pytest

from decider.jev_client import JevClient
from decider.jev_selector import JevSelector


@pytest.fixture
def mock_client():
    return MagicMock(spec=JevClient)


@pytest.fixture
def selector(mock_client):
    return JevSelector(client=mock_client)


def test_jev_selector_call_tool(selector, mock_client, sample_tool_candidates):
    mock_client.post_decision.return_value = {
        "code": 0,
        "message": "ok",
        "data": {"answers": {"tool_choice": {"choice": "calculator", "confidence": 0.95}}},
    }

    decision = selector.select("Calculate 1 + 1", sample_tool_candidates)

    assert decision.decision == "call_tool"
    assert decision.tool == "calculator"
    assert decision.confidence == 0.95
    assert "Jev selected candidate tool" in decision.reason


def test_jev_selector_no_tool(selector, mock_client, sample_tool_candidates):
    mock_client.post_decision.return_value = {
        "code": 0,
        "message": "ok",
        "data": {"answers": {"tool_choice": {"choice": "no_tool", "confidence": 0.88}}},
    }

    decision = selector.select("What is MCP?", sample_tool_candidates)

    assert decision.decision == "no_tool"
    assert decision.tool is None
    assert decision.confidence == 0.88
    assert "Jev routed to no_tool" in decision.reason


def test_jev_selector_unknown_candidate(selector, mock_client, sample_tool_candidates):
    mock_client.post_decision.return_value = {
        "code": 0,
        "message": "ok",
        "data": {"answers": {"tool_choice": {"choice": "non_existent_tool", "confidence": 0.9}}},
    }

    decision = selector.select("Do something", sample_tool_candidates)

    assert decision.decision == "cannot_decide"
    assert decision.tool is None
    assert "unknown candidate: non_existent_tool" in decision.reason


def test_jev_selector_api_error(selector, mock_client, sample_tool_candidates):
    mock_client.post_decision.side_effect = RuntimeError("Connection failed")

    decision = selector.select("Calculate something", sample_tool_candidates)

    assert decision.decision == "cannot_decide"
    assert decision.tool is None
    assert "Jev API failure: Connection failed" in decision.reason
