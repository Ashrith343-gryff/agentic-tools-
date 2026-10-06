"""
Ranking demo for agentic-tool-decider.
"""

from decider.models import ToolCandidate
from decider.ranking import rank_candidates


def main() -> None:
    candidates = [
        ToolCandidate(
            name="calculator",
            description="Performs arithmetic calculations such as addition, subtraction, multiplication, and division",
            input_schema={},
        ),
        ToolCandidate(
            name="sqlite_query",
            description="Executes read-only SQL queries against a local SQLite database",
            input_schema={},
        ),
        ToolCandidate(
            name="search_knowledge",
            description="Searches a local knowledge base of workshop documents using semantic retrieval",
            input_schema={},
        )
    ]

    request = "Find information about MCP in the workshop documents"
    print(f"Request: {request}\n")

    ranked, scores = rank_candidates(request, candidates)

    print("Ranking Results:")
    for i, candidate in enumerate(ranked):
        print(f"{i + 1}. {candidate.name} (Score: {scores[candidate.name]:.2f})")
        print(f"   Description: {candidate.description}")


if __name__ == "__main__":
    main()
