"""
Decision demo for agentic-tool-decider.
"""

from decider.decision import Decision, DecisionEngine, MockSelector
from decider.schema import ToolCandidate

from decider.registry import ToolRegistry


def main() -> None:
    # 1. Create registry
    registry = ToolRegistry()

    # 2. Register candidates
    registry.register(
        ToolCandidate(
            name="calculator",
            description="Performs arithmetic operations",
            schema={"type": "object", "properties": {"expression": {"type": "string"}}},
        )
    )
    registry.register(
        ToolCandidate(
            name="sqlite_query",
            description="Executes a query against a local sqlite db",
            schema={"type": "object", "properties": {"query": {"type": "string"}}},
        )
    )

    # 3. Create engine with mock selector
    engine = DecisionEngine(selector=MockSelector())

    # 4. Submit user request
    request = "Calculate 12 * 5"
    print(f"Request: {request}")

    # 5. Receive Decision
    decision: Decision = engine.decide(request=request, candidates=registry.list_candidates())

    # 6. Print structured result
    print("Decision:")
    print(f"  Selected Tool: {decision.selected_tool}")
    print(f"  Arguments: {decision.arguments}")
    print(f"  Reasoning: {decision.reasoning}")


if __name__ == "__main__":
    main()
