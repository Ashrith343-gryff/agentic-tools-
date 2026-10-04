import pytest

from decider.handoff import HandoffManager
from decider.models import AgentRoute, Handoff
from decider.routing import CycleDetectedError, RouteManager


def test_create_handoff_success():
    route_manager = RouteManager()
    handoff_manager = HandoffManager(route_manager)

    route = AgentRoute("source_agent", "target_agent", "needs help")
    handoff = handoff_manager.create_handoff(route, {"data": "test"})

    assert isinstance(handoff, Handoff)
    assert handoff.status == "pending"
    assert handoff.context == {"data": "test"}
    assert handoff.route == route


def test_create_handoff_fails_on_cycle():
    route_manager = RouteManager()
    handoff_manager = HandoffManager(route_manager)

    # First valid handoff
    handoff_manager.create_handoff(AgentRoute("A", "B", "ok"), {})

    # Second handoff causing a cycle
    with pytest.raises(CycleDetectedError):
        handoff_manager.create_handoff(AgentRoute("B", "A", "loop"), {})
