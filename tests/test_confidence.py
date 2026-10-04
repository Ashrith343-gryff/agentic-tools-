from decider.confidence import apply_confidence_gate
from decider.models import Decision


def test_confidence_gate_passes():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=0.95
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result == decision


def test_confidence_gate_exact_threshold():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=0.80
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result == decision


def test_confidence_gate_fails():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=0.79
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result.decision == "cannot_decide"
    assert result.tool is None
    assert "below threshold" in result.reason
    assert result.confidence == 0.79


def test_confidence_gate_missing_confidence():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=None
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result.decision == "cannot_decide"
    assert "Missing confidence" in result.reason


def test_confidence_gate_negative_confidence():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=-0.1
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result.decision == "cannot_decide"
    assert "Invalid confidence score" in result.reason


def test_confidence_gate_over_one():
    decision = Decision(
        decision="call_tool", tool="calculator", arguments={}, reason="ok", confidence=1.5
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result.decision == "cannot_decide"
    assert "Invalid confidence score" in result.reason


def test_confidence_gate_already_cannot_decide():
    decision = Decision(
        decision="cannot_decide", tool=None, arguments={}, reason="already failed", confidence=None
    )
    result = apply_confidence_gate(decision, 0.80)
    assert result == decision
