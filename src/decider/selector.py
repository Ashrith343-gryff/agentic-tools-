from abc import ABC, abstractmethod

from .models import Decision, ToolCandidate


class Selector(ABC):
    """Abstract base class for a tool selector."""

    @abstractmethod
    def select(self, request: str, candidates: list[ToolCandidate]) -> Decision:
        """Select a tool based on the user request and available candidates.

        Args:
            request: The user's request text.
            candidates: A list of available ToolCandidate objects.

        Returns:
            A Decision object representing the tool selection outcome.
        """
        pass
