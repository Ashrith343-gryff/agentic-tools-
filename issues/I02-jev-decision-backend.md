# I02 — Jev Decision Backend

## Goal
Integrate Jev as an OPTIONAL decision backend.

## Requirements:
- Jev is a decision service, NOT the tool executor.
- Jev is NOT the main agent model.
- Use the documented HTTP API (`POST /api/v1/decisions`).
- Jev responses must be converted into our internal Decision model.
- Must support tests using mocked HTTP responses (no network required for tests).
