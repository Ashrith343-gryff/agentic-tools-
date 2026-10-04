from .models import AgentRoute


class RoutingException(Exception):
    """Base exception for routing errors."""

    pass


class CycleDetectedError(RoutingException):
    """Raised when a routing cycle is detected."""

    pass


class MaxHopsExceededError(RoutingException):
    """Raised when the maximum routing hop limit is exceeded."""

    pass


class RouteManager:
    """Manages routing history and validates new routes for cycles and hop limits."""

    def __init__(self, max_hops: int = 5):
        self.max_hops = max_hops
        self.history: list[AgentRoute] = []

    def validate_and_add_route(self, route: AgentRoute) -> None:
        """Validate a new route against history and add it if valid.

        Args:
            route: The new AgentRoute to validate.

        Raises:
            MaxHopsExceededError: If adding this route exceeds max_hops.
            CycleDetectedError: If this route loops back to an already visited agent.
        """
        if len(self.history) >= self.max_hops:
            raise MaxHopsExceededError(f"Maximum routing limit of {self.max_hops} hops exceeded.")

        # Determine all unique agents that have already been involved
        seen = set()
        for r in self.history:
            seen.add(r.source)
            seen.add(r.target)

        # Include the current route's source
        seen.add(route.source)

        if route.target in seen:
            path = " -> ".join([r.source for r in self.history] + [route.source, route.target])
            raise CycleDetectedError(f"Routing cycle detected: {path}")

        self.history.append(route)
