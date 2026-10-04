import pytest

from decider.models import AgentRoute, Decision, Handoff, ToolCandidate, ToolSelection


def test_decision_creation_and_dict(
    sample_decision_call_tool, sample_decision_no_tool, sample_decision_cannot_decide
):
    for dec in [sample_decision_call_tool, sample_decision_no_tool, sample_decision_cannot_decide]:
        d = dec.to_dict()
        assert Decision.from_dict(d).to_dict() == d


def test_invalid_decision():
    with pytest.raises(ValueError, match="Invalid decision"):
        Decision(decision="maybe", tool=None, arguments={}, reason="nope")


def test_call_tool_requires_tool_name():
    with pytest.raises(ValueError, match="requires a tool name"):
        Decision(decision="call_tool", tool=None, arguments={}, reason="forgot tool")


def test_tool_candidate(sample_tool_candidates):
    tc = sample_tool_candidates[0]
    d = tc.to_dict()
    assert ToolCandidate.from_dict(d).to_dict() == d


def test_tool_selection(sample_tool_candidates, sample_decision_call_tool):
    ts = ToolSelection(
        request="calculate 2+2",
        candidates=sample_tool_candidates,
        decision=sample_decision_call_tool,
        scores={"calculator": 0.99},
    )
    d = ts.to_dict()
    ts2 = ToolSelection.from_dict(d)
    assert ts2.request == ts.request
    assert len(ts2.candidates) == len(ts.candidates)
    assert ts2.decision.decision == ts.decision.decision


def test_agent_route():
    route = AgentRoute(source="agentA", target="agentB", reason="handoff needed", confidence=0.8)
    d = route.to_dict()
    assert AgentRoute.from_dict(d).to_dict() == d


def test_handoff():
    route = AgentRoute(source="agentA", target="agentB", reason="handoff needed")
    handoff = Handoff(route=route, context={"user_id": 123}, status="pending")
    d = handoff.to_dict()
    assert Handoff.from_dict(d).to_dict() == d


def test_invalid_handoff_status():
    route = AgentRoute(source="agentA", target="agentB", reason="handoff needed")
    with pytest.raises(ValueError, match="Invalid status"):
        Handoff(route=route, context={}, status="maybe")
