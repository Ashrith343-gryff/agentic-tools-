from decider.models import Decision, ToolCandidate
from decider.selector import Selector


class DummySelector(Selector):
    def select(self, request: str, candidates: list[ToolCandidate]) -> Decision:
        return Decision(decision="no_tool", tool=None, arguments={}, reason="dummy")


def test_selector_interface():
    # Verify that we can inherit and implement the ABC
    selector = DummySelector()
    decision = selector.select("test", [])
    assert decision.decision == "no_tool"
    assert decision.reason == "dummy"
