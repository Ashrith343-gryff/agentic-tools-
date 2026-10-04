from .jev_client import JevClient
from .models import Decision, ToolCandidate
from .selector import Selector


class JevSelector(Selector):
    """A tool selector backed by the Jev API."""

    def __init__(self, client: JevClient):
        self.client = client

    def select(self, request: str, candidates: list[ToolCandidate]) -> Decision:
        """Select a tool using the Jev API native decisions endpoint."""

        # Build criteria mapping
        criteria = {c.name: c.description for c in candidates}
        criteria["no_tool"] = "The request can be answered without a tool."
        criteria["cannot_decide"] = "The request is unsupported or too ambiguous."

        payload = {
            "state": {"request": request},
            "questions": {
                "tool_choice": {
                    "type": "choice",
                    "instructions": "Select the best tool capability for the request.",
                    "criteria": criteria,
                }
            },
        }

        try:
            response = self.client.post_decision("/api/v1/decisions", payload)
        except RuntimeError as e:
            # On API failure, safely degrade or report cannot_decide
            return Decision(
                decision="cannot_decide",
                tool=None,
                arguments={},
                reason=f"Jev API failure: {str(e)}",
            )

        data = response.get("data", {})

        # Depending on whether the response is a native decisions response or preset
        if "answers" in data:
            tool_choice = data.get("answers", {}).get("tool_choice", {})
            choice = tool_choice.get("choice")
            confidence = tool_choice.get("confidence")
        else:
            # Fallback if using a preset style response
            choice = data.get("decision")
            confidence = data.get("confidence")

        if not choice:
            return Decision(
                decision="cannot_decide",
                tool=None,
                arguments={},
                reason="Jev returned an empty or malformed choice",
                confidence=None,
            )

        if choice in ("no_tool", "cannot_decide"):
            return Decision(
                decision=choice,
                tool=None,
                arguments={},
                reason=f"Jev routed to {choice}",
                confidence=confidence,
            )

        # Ensure the selected choice actually matches a valid candidate
        if any(c.name == choice for c in candidates):
            return Decision(
                decision="call_tool",
                tool=choice,
                arguments={},
                reason="Jev selected candidate tool",
                confidence=confidence,
            )

        return Decision(
            decision="cannot_decide",
            tool=None,
            arguments={},
            reason=f"Jev returned unknown candidate: {choice}",
            confidence=confidence,
        )
