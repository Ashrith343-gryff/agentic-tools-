import pytest

from decider.mock_selector import MockSelector


@pytest.fixture
def mock_selector():
    return MockSelector()


def test_mock_selector_arithmetic(mock_selector, sample_tool_candidates):
    decision = mock_selector.select("Calculate 12 * 5", sample_tool_candidates)
    assert decision.decision == "call_tool"
    assert decision.tool == "calculator"
    assert decision.reason == "request requires arithmetic"


def test_mock_selector_knowledge(mock_selector, sample_tool_candidates):
    decision = mock_selector.select("What is MCP?", sample_tool_candidates)
    assert decision.decision == "no_tool"
    assert decision.tool is None
    assert decision.reason == "request can be answered without a tool"


def test_mock_selector_retrieval(mock_selector, sample_tool_candidates):
    decision = mock_selector.select(
        "Find information about MCP in the workshop documents", sample_tool_candidates
    )
    assert decision.decision == "call_tool"
    assert decision.tool == "search_knowledge"
    assert decision.reason == "request requires searching workshop documents"


def test_mock_selector_ambiguous(mock_selector, sample_tool_candidates):
    decision = mock_selector.select("Help me with my project", sample_tool_candidates)
    assert decision.decision == "cannot_decide"
    assert decision.tool is None
    assert decision.reason == "request is too ambiguous to select a tool"


def test_mock_selector_unsupported(mock_selector, sample_tool_candidates):
    decision = mock_selector.select(
        "Book a flight to Tokyo for next Tuesday", sample_tool_candidates
    )
    assert decision.decision == "cannot_decide"
    assert decision.tool is None
    assert decision.reason == "no registered capability matches the request"


def test_mock_selector_missing_tool(mock_selector):
    # Request asks for calculator but it's not in candidates
    decision = mock_selector.select("Calculate 12 * 5", [])
    assert decision.decision == "cannot_decide"
    assert decision.tool is None
    assert decision.reason == "no registered capability matches the request"
