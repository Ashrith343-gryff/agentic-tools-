import pytest

from decider.models import Decision, ToolCandidate


@pytest.fixture
def sample_tool_candidates():
    return [
        ToolCandidate(
            name="calculator",
            description="Perform basic arithmetic.",
            input_schema={
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        ),
        ToolCandidate(
            name="sqlite_query",
            description="Run a read-only query on a SQLite DB.",
            input_schema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        ToolCandidate(
            name="search_knowledge",
            description="Search the knowledge base.",
            input_schema={
                "type": "object",
                "properties": {"q": {"type": "string"}},
                "required": ["q"],
            },
        ),
    ]


@pytest.fixture
def sample_decision_call_tool():
    return Decision(
        decision="call_tool",
        tool="calculator",
        arguments={"expression": "2+2"},
        reason="User asked for calculation",
        confidence=0.99,
    )


@pytest.fixture
def sample_decision_no_tool():
    return Decision(
        decision="no_tool",
        tool=None,
        arguments={},
        reason="General greeting, no tool needed",
        confidence=0.9,
    )


@pytest.fixture
def sample_decision_cannot_decide():
    return Decision(
        decision="cannot_decide",
        tool=None,
        arguments={},
        reason="Ambiguous request",
        confidence=0.1,
    )
