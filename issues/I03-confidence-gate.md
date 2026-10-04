# I03 — Confidence Gate

## Goal
Implement a confidence gate to evaluate whether a tool decision should be allowed.

## Requirements:
- Compare the decision's confidence score against a configured threshold (e.g., 0.80).
- If confidence >= threshold: allow decision.
- If confidence < threshold: return `cannot_decide`.
- Handle edge cases: missing confidence, negative confidence, confidence > 1.0.
