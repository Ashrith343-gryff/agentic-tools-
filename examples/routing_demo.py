"""
Routing and handoff demo for agentic-tool-decider.
"""

from decider.models import AgentRoute
from decider.routing import RouteManager, CycleDetectedError, MaxHopsExceededError
from decider.handoff import HandoffManager


def main() -> None:
    route_manager = RouteManager(max_hops=3)
    handoff_manager = HandoffManager(route_manager)

    print("--- Scenario 1: Valid Chain ---")
    route1 = AgentRoute(source="main_agent", target="research_agent", reason="Needs deep research")
    handoff1 = handoff_manager.create_handoff(route1, context={"query": "MCP docs"})
    print(f"Created handoff: {handoff1.route.source} -> {handoff1.route.target}")

    route2 = AgentRoute(source="research_agent", target="summarize_agent", reason="Research complete, please summarize")
    handoff2 = handoff_manager.create_handoff(route2, context={"notes": "MCP is cool"})
    print(f"Created handoff: {handoff2.route.source} -> {handoff2.route.target}")

    print("\n--- Scenario 2: Cycle Detection ---")
    route3 = AgentRoute(source="summarize_agent", target="main_agent", reason="Returning to main")
    try:
        handoff_manager.create_handoff(route3, context={})
    except CycleDetectedError as e:
        print(f"Successfully blocked cycle! Error: {e}")

    print("\n--- Scenario 3: Hop Limit Exceeded ---")
    route_manager_short = RouteManager(max_hops=1)
    hm_short = HandoffManager(route_manager_short)
    
    hm_short.create_handoff(AgentRoute("A", "B", "First hop"), {})
    try:
        hm_short.create_handoff(AgentRoute("B", "C", "Second hop"), {})
    except MaxHopsExceededError as e:
        print(f"Successfully blocked excessive hops! Error: {e}")


if __name__ == "__main__":
    main()
