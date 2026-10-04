from .models import ToolCandidate


class ToolRegistry:
    """Registry for managing available tool capabilities."""

    def __init__(self):
        self._tools: dict[str, ToolCandidate] = {}

    def register(self, candidate: ToolCandidate) -> None:
        """Register a new tool candidate.

        Args:
            candidate: The ToolCandidate to register.

        Raises:
            ValueError: If a tool with the same name is already registered.
        """
        if candidate.name in self._tools:
            raise ValueError(f"Tool '{candidate.name}' is already registered.")
        self._tools[candidate.name] = candidate

    def get_tool(self, name: str) -> ToolCandidate:
        """Retrieve a tool by name.

        Args:
            name: The name of the tool to retrieve.

        Returns:
            The requested ToolCandidate.

        Raises:
            KeyError: If the tool is not found.
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def list_tools(self) -> list[ToolCandidate]:
        """List all registered tool candidates.

        Returns:
            A list of all registered ToolCandidates.
        """
        return list(self._tools.values())

    def remove_tool(self, name: str) -> None:
        """Remove a tool from the registry.

        Args:
            name: The name of the tool to remove.

        Raises:
            KeyError: If the tool is not found.
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        del self._tools[name]
