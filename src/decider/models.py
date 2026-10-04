from dataclasses import dataclass, field
from typing import Any


@dataclass
class Decision:
    decision: str
    tool: str | None
    arguments: dict[str, Any]
    reason: str
    confidence: float | None = None

    def __post_init__(self):
        if self.decision not in ("call_tool", "no_tool", "cannot_decide"):
            raise ValueError(f"Invalid decision: {self.decision}")
        if self.decision == "call_tool" and not self.tool:
            raise ValueError("Decision 'call_tool' requires a tool name")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "tool": self.tool,
            "arguments": self.arguments,
            "reason": self.reason,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Decision":
        return cls(
            decision=data["decision"],
            tool=data.get("tool"),
            arguments=data.get("arguments", {}),
            reason=data["reason"],
            confidence=data.get("confidence"),
        )


@dataclass
class ToolCandidate:
    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.input_schema,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolCandidate":
        return cls(
            name=data["name"],
            description=data["description"],
            input_schema=data["input_schema"],
        )


@dataclass
class ToolSelection:
    request: str
    candidates: list[ToolCandidate]
    decision: Decision
    scores: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request,
            "candidates": [c.to_dict() for c in self.candidates],
            "decision": self.decision.to_dict(),
            "scores": self.scores,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToolSelection":
        return cls(
            request=data["request"],
            candidates=[ToolCandidate.from_dict(c) for c in data["candidates"]],
            decision=Decision.from_dict(data["decision"]),
            scores=data.get("scores", {}),
        )


@dataclass
class AgentRoute:
    source: str
    target: str
    reason: str
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "reason": self.reason,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentRoute":
        return cls(
            source=data["source"],
            target=data["target"],
            reason=data["reason"],
            confidence=data.get("confidence"),
        )


@dataclass
class Handoff:
    route: AgentRoute
    context: dict[str, Any]
    status: str

    def __post_init__(self):
        if self.status not in ("pending", "accepted", "rejected"):
            raise ValueError(f"Invalid status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "route": self.route.to_dict(),
            "context": self.context,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Handoff":
        return cls(
            route=AgentRoute.from_dict(data["route"]),
            context=data.get("context", {}),
            status=data["status"],
        )
