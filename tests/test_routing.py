import pytest

from decider.models import AgentRoute
from decider.routing import CycleDetectedError, MaxHopsExceededError, RouteManager


def test_valid_routing_chain():
    manager = RouteManager(max_hops=3)
    manager.validate_and_add_route(AgentRoute("A", "B", "reason 1"))
    manager.validate_and_add_route(AgentRoute("B", "C", "reason 2"))
    manager.validate_and_add_route(AgentRoute("C", "D", "reason 3"))

    assert len(manager.history) == 3


def test_self_cycle():
    manager = RouteManager()
    with pytest.raises(CycleDetectedError, match="A -> A"):
        manager.validate_and_add_route(AgentRoute("A", "A", "self loop"))


def test_simple_cycle():
    manager = RouteManager()
    manager.validate_and_add_route(AgentRoute("A", "B", "ok"))
    with pytest.raises(CycleDetectedError, match="A -> B -> A"):
        manager.validate_and_add_route(AgentRoute("B", "A", "loop back"))


def test_complex_cycle():
    manager = RouteManager()
    manager.validate_and_add_route(AgentRoute("A", "B", "ok"))
    manager.validate_and_add_route(AgentRoute("B", "C", "ok"))
    manager.validate_and_add_route(AgentRoute("C", "D", "ok"))

    with pytest.raises(CycleDetectedError, match="A -> B -> C -> D -> B"):
        manager.validate_and_add_route(AgentRoute("D", "B", "loop back to B"))


def test_max_hops_exceeded():
    manager = RouteManager(max_hops=2)
    manager.validate_and_add_route(AgentRoute("A", "B", "hop 1"))
    manager.validate_and_add_route(AgentRoute("B", "C", "hop 2"))

    with pytest.raises(MaxHopsExceededError, match="Maximum routing limit of 2 hops exceeded"):
        manager.validate_and_add_route(AgentRoute("C", "D", "hop 3"))
