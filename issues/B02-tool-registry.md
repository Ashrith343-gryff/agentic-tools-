# B02 — Tool Registry

## Goal
Implement a capability registry.

A `ToolCandidate` should contain:
- name
- description
- input_schema

## Registry operations:
- `register()`
- `get_tool()`
- `list_tools()`
- `remove_tool()`

The registry describes capabilities. It MUST NOT execute tools.

## Tests must cover:
- registration
- retrieval
- listing
- removal
- duplicate names
- missing tools
- malformed definitions
