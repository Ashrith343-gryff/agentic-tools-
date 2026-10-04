"""
Ranking demo for agentic-tool-decider.
"""

from decider.decision import DecisionEngine, MockSelector
from decider.schema import ToolCandidate


def main() -> None:
    candidates = [
        ToolCandidate("search", "Search the web", {}),
        ToolCandidate("weather", "Get the weather", {}),
        ToolCandidate("calculator", "Calculate math expressions", {}),
    ]

    engine = DecisionEngine(selector=MockSelector())

    request = "What is the weather in Tokyo?"
    print(f"Request: {request}")

    # The MockSelector doesn't naturally do scoring, so we just show the output.
    decision = engine.decide(request, candidates)

    print("\nCandidates considered:")
    for c in candidates:
        print(f" - {c.name}: {c.description}")

    print(f"\nTop choice based on mock logic: {decision.selected_tool}")


if __name__ == "__main__":
    main()
