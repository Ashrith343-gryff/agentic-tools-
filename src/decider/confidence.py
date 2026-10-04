from .models import Decision


def apply_confidence_gate(decision: Decision, threshold: float) -> Decision:
    """Evaluate a decision against a confidence threshold.

    If the decision's confidence is below the threshold, missing, or invalid,
    this returns a new 'cannot_decide' decision.

    Args:
        decision: The original Decision object.
        threshold: The required minimum confidence score (0.0 to 1.0).

    Returns:
        The original Decision if it passes, otherwise a 'cannot_decide' Decision.
    """
    if decision.decision == "cannot_decide":
        return decision

    conf = decision.confidence

    if conf is None:
        return Decision(
            decision="cannot_decide",
            tool=None,
            arguments={},
            reason=f"Missing confidence score, required threshold {threshold}",
            confidence=None,
        )

    if not (0.0 <= conf <= 1.0):
        return Decision(
            decision="cannot_decide",
            tool=None,
            arguments={},
            reason=f"Invalid confidence score {conf}, must be between 0.0 and 1.0",
            confidence=conf,
        )

    if conf < threshold:
        return Decision(
            decision="cannot_decide",
            tool=None,
            arguments={},
            reason=f"Confidence {conf} below threshold {threshold}",
            confidence=conf,
        )

    return decision
