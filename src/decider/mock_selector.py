from .models import Decision, ToolCandidate
from .selector import Selector


class MockSelector(Selector):
    """A deterministic mock selector for testing and offline execution.

    Uses simple keyword matching to select tools based on the expected workshop examples.
    Requires no network access, API keys, or hosted models.
    """

    def select(self, request: str, candidates: list[ToolCandidate]) -> Decision:
        req_lower = request.lower()
        candidate_names = {c.name for c in candidates}

        # Arithmetic request
        if "calculate" in req_lower or "*" in req_lower or "+" in req_lower:
            if "calculator" in candidate_names:
                return Decision(
                    decision="call_tool",
                    tool="calculator",
                    arguments={},
                    reason="request requires arithmetic",
                )

        # Knowledge retrieval request
        if "find" in req_lower or "search" in req_lower or "workshop" in req_lower:
            if "search_knowledge" in candidate_names:
                return Decision(
                    decision="call_tool",
                    tool="search_knowledge",
                    arguments={},
                    reason="request requires searching workshop documents",
                )

        # Database query request
        if "query" in req_lower or "sql" in req_lower or "database" in req_lower:
            if "sqlite_query" in candidate_names:
                return Decision(
                    decision="call_tool",
                    tool="sqlite_query",
                    arguments={},
                    reason="request requires database query",
                )

        # General knowledge request that doesn't need a tool
        if "what is" in req_lower or "explain" in req_lower:
            return Decision(
                decision="no_tool",
                tool=None,
                arguments={},
                reason="request can be answered without a tool",
            )

     # Ambiguous request check
if ("help" in req_lower and "project" in req_lower) or "do something" in req_lower or "ambiguous" in req_lower:
    return Decision(
        decision="cannot_decide",
        tool=None,
        arguments={},
        reason="request is too ambiguous to select a tool",
    )

# Fallback for unsupported / unknown request
return Decision(
    decision="cannot_decide",
    tool=None,
    arguments={},
    reason="no registered capability matches the request",
)
