# B03 — Deterministic Tool Selector

## Goal
Implement the Selector interface and a deterministic MockSelector.

The selector receives:
- user request
- available tool candidates

It returns:
- `Decision`

## Examples:
- "Calculate 12 * 5" → `call_tool` / calculator
- "What is MCP?" → `no_tool`
- "Do something impossible" → `cannot_decide`

## Requirements:
The mock selector must be deterministic.
It must require:
- no internet
- no API key
- no hosted model

This is the default contributor and CI mode.
