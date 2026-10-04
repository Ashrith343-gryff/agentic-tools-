# A01 — Agent Routing, Handoff & Cycle Detection

## Goal
Implement routing and handoff logic, along with cycle detection.

## Requirements:
- Support decisions like `main_agent -> research_agent`.
- Represent source, target, reason, confidence in `AgentRoute`.
- Represent `Handoff`.
- Implement cycle detection to reject loops (e.g., A -> A, A -> B -> A, A -> B -> C -> A).
- Implement a configurable maximum hop limit.
- Routing and handoff MUST NOT execute agents. They only create and validate routing decisions.
