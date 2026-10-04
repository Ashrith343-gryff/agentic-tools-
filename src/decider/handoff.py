from .models import AgentRoute, Handoff
from .routing import RouteManager


class HandoffManager:
    """Creates and manages agent handoffs safely without executing agents."""

    def __init__(self, route_manager: RouteManager):
        self.route_manager = route_manager

    def create_handoff(self, route: AgentRoute, context: dict) -> Handoff:
        """Create a new handoff after validating the route.

        Args:
            route: The AgentRoute defining source and target.
            context: Any context payload to pass during handoff.

        Returns:
            A new Handoff object with status 'pending'.

        Raises:
            RoutingException: If the route is invalid (cycles, max hops).
        """
        # Validate route first
        self.route_manager.validate_and_add_route(route)

        return Handoff(route=route, context=context, status="pending")
