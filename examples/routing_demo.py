"""
Routing demo for agentic-tool-decider.
"""

from decider.router import RouteCandidate, Router


def main() -> None:
    router = Router()

    candidates = [
        RouteCandidate(name="agent_a", description="Handles math", target_id="agent_a"),
        RouteCandidate(name="agent_b", description="Handles text", target_id="agent_b"),
    ]

    print("Demonstrating routing to agent_a...")
    route_path = router.route("I need math help", candidates)

    print(f"Routed to: {route_path.target_id}")

    print("\nDemonstrating handoff validation...")
    print("Adding handoff from parent -> agent_a")
    router.record_handoff("parent", "agent_a")
    print("History:", router.get_history())

    print("\nAdding handoff from agent_a -> agent_b")
    router.record_handoff("agent_a", "agent_b")
    print("History:", router.get_history())

    print("\nTrying to handoff from agent_b -> parent (cycle)...")
    try:
        router.record_handoff("agent_b", "parent")
    except ValueError as e:
        print(f"Cycle detected as expected: {e}")


if __name__ == "__main__":
    main()
