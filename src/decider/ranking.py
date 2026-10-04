from .models import ToolCandidate


def rank_candidates(
    request: str, candidates: list[ToolCandidate]
) -> tuple[list[ToolCandidate], dict[str, float]]:
    """Rank tool candidates deterministically based on the request.

    Args:
        request: The user's request.
        candidates: A list of available ToolCandidate objects.

    Returns:
        A tuple containing:
        - The sorted list of candidates (highest score first).
        - A dictionary mapping tool names to their computed scores.
    """
    scores = {}
    req_lower = request.lower()

    for candidate in candidates:
        score = 0.0

        # Simple deterministic scoring heuristics based on tool names
        if candidate.name == "search_knowledge" and (
            "search" in req_lower or "workshop" in req_lower or "find" in req_lower
        ):
            score += 2.0
        if candidate.name == "calculator" and ("calculate" in req_lower or "*" in req_lower):
            score += 2.0
        if candidate.name == "sqlite_query" and ("query" in req_lower or "sql" in req_lower):
            score += 2.0

        # Give a small base score based on keyword matches in the description
        for word in candidate.description.lower().split():
            if len(word) > 3 and word in req_lower:
                score += 0.5

        scores[candidate.name] = score

    # Sort candidates by score (descending), then by name (ascending) for stable ordering of ties
    ranked = sorted(candidates, key=lambda c: (-scores[c.name], c.name))

    return ranked, scores
