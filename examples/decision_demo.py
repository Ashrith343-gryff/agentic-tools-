"""
Decision demo for agentic-tool-decider.
"""

import json
from decider.models import ToolCandidate, Decision
from decider.registry import ToolRegistry
from decider.mock_selector import MockSelector


def main() -> None:
    # 1. Create registry
    registry = ToolRegistry()

    # 2. Register candidates
    registry.register(
        ToolCandidate(
            name="calculator",
            description="Performs arithmetic calculations such as addition, subtraction, multiplication, and division",
            input_schema={"type": "object", "properties": {"expression": {"type": "string"}}},
        )
    )
    registry.register(
        ToolCandidate(
            name="sqlite_query",
            description="Executes read-only SQL queries against a local SQLite database",
            input_schema={"type": "object", "properties": {"query": {"type": "string"}}},
        )
    )

    # 3. Create mock selector
    selector = MockSelector()

    # 4. Submit user request
    request = "Calculate 12 * 5"
    print(f"Request: {request}")

    # 5. Receive Decision
    decision: Decision = selector.select(request=request, candidates=registry.list_tools())

    # 6. Print structured result
    print("\nDecision Result:")
    print(json.dumps(decision.to_dict(), indent=2))


if __name__ == "__main__":
    main()
