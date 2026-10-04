import pytest

from decider.models import ToolCandidate
from decider.registry import ToolRegistry


@pytest.fixture
def registry():
    return ToolRegistry()


@pytest.fixture
def calculator_tool():
    return ToolCandidate(
        name="calculator",
        description="Performs arithmetic",
        input_schema={"type": "object", "properties": {"expression": {"type": "string"}}},
    )


@pytest.fixture
def db_tool():
    return ToolCandidate(
        name="sqlite_query",
        description="Executes SQL",
        input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
    )


def test_register_and_get_tool(registry, calculator_tool):
    registry.register(calculator_tool)
    retrieved = registry.get_tool("calculator")
    assert retrieved == calculator_tool


def test_register_duplicate_tool(registry, calculator_tool):
    registry.register(calculator_tool)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(calculator_tool)


def test_get_missing_tool(registry):
    with pytest.raises(KeyError, match="not found"):
        registry.get_tool("missing_tool")


def test_list_tools(registry, calculator_tool, db_tool):
    assert len(registry.list_tools()) == 0
    registry.register(calculator_tool)
    registry.register(db_tool)

    tools = registry.list_tools()
    assert len(tools) == 2
    assert calculator_tool in tools
    assert db_tool in tools


def test_remove_tool(registry, calculator_tool):
    registry.register(calculator_tool)
    assert len(registry.list_tools()) == 1

    registry.remove_tool("calculator")
    assert len(registry.list_tools()) == 0

    with pytest.raises(KeyError, match="not found"):
        registry.get_tool("calculator")


def test_remove_missing_tool(registry):
    with pytest.raises(KeyError, match="not found"):
        registry.remove_tool("missing_tool")
