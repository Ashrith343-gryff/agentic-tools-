# Agentic Tool Decider

## What is this?
The Agentic Tool Decider is a lightweight, self-contained Python component that determines which tool an AI agent should use next, based on the current context, user query, and available tools. It acts as the brain's decision-making center, abstracting the complex process of tool selection away from the main agent loop.

## Why a Tool Decider?
In complex agent architectures, the logic for deciding *what to do next* often gets tangled with the logic for *executing* tasks. The Tool Decider separates these concerns. It only decides; it never executes. This makes the system easier to test, debug, and upgrade.

## Architecture
The system is built on a modular architecture:
- **Registry:** Manages the list of available tools.
- **Selector:** Evaluates tools against a query (supports both local/deterministic and remote LLM-based selection).
- **Ranking:** Orders tools based on relevance.
- **Gate:** Applies confidence thresholds to prevent risky actions.

## Decision Flow
1. The Agent Runtime receives a user request.
2. The Runtime queries the Tool Decider with the context.
3. The Decider evaluates registered tools using its Selectors.
4. The Decider returns a ranked list or a single chosen tool with a confidence score.
5. The Runtime (or caller) executes the chosen tool.

## Repository Structure
```
src/decider/
  __init__.py
  models.py
  registry.py
  selectors/
    __init__.py
    base.py
    mock.py
    jev.py
  ranking/
    ...
tests/
  ...
docs/
  ...
```

## Quick Start
1. Clone the repository.
2. Ensure you have Python 3.12 installed.
3. Create a virtual environment: `python -m venv .venv` and activate it.
4. Install dependencies (e.g., using `pip install -e .` or simply running without external libs if self-contained).
5. Run tests: `pytest`

## Seven Official Contributor Issues
This repository was designed around exactly seven main implementation issues for workshop contributors to solve. The reference solutions are implemented in this repository, and the issue descriptions can be found in the `issues/` directory:
- [B01 — Decision Models & Contracts](issues/B01-decision-models.md)
- [B02 — Tool Registry](issues/B02-tool-registry.md)
- [B03 — Deterministic Tool Selector](issues/B03-deterministic-tool-selector.md)
- [I01 — Tool Ranking & Candidate Selection](issues/I01-tool-ranking.md)
- [I02 — Jev Decision Backend](issues/I02-jev-decision-backend.md)
- [I03 — Confidence Gate](issues/I03-confidence-gate.md)
- [A01 — Agent Routing, Handoff & Cycle Detection](issues/A01-routing-handoff.md)

## Offline Mode
You do not need an API key to run this repository. By default, you can run the system entirely offline using the Mock mode (`DECIDER_MODE=mock`). This is fully deterministic and excellent for local testing and CI/CD pipelines.

## Tool Registry
The `Registry` stores tool schemas (often JSON Schema) and metadata. It acts as the single source of truth for what actions are available to the agent.

## Deterministic Selector
The `MockSelector` provides deterministic, rule-based or heuristic-based tool selection without requiring external network calls. It's the default offline selector.

## Tool Ranking
When multiple tools might be applicable, the ranking engine scores them based on relevance to the query, historical success, or simple keyword matching.

## Jev Integration
For more advanced, AI-driven decision-making, the decider supports integration with Jev AI.
You can enable this by setting `DECIDER_MODE=jev` and providing `JEV_API_KEY=your_own_key`.
For more details, see the [Jev AI Documentation](https://www.jevai.org/docs).

## API Keys
The system can run completely without API keys in Mock mode.
If using Jev mode, you must provide your own API key. **Never commit your API key.**
See `docs/api-keys.md` for a complete guide.

## Confidence Gate
The Confidence Gate prevents the agent from taking actions when it isn't sure. If the selector's confidence score falls below a configured threshold, the decision is rejected or handed back to the user.

## Agent Routing
The decider can also be used to route requests between specialized sub-agents by treating agents themselves as "tools" in the registry.

## Handoff
If no tool is suitable, or confidence is too low, the decider returns a Handoff signal, gracefully returning control to the user or a human operator.

## Cycle Detection
To prevent agents from getting stuck in infinite loops (e.g., calling the same tool repeatedly with the same arguments), the decider includes cycle detection logic.

## Testing
All tests are local and deterministic. Run `pytest` to execute the test suite. No network required.

## Contributing
We welcome contributions! Please see `CONTRIBUTING.md` for guidelines on how to fork, branch, and submit Pull Requests.

## Security
Security is a top priority. See `SECURITY.md` for our responsible disclosure policy and guidelines on handling API keys safely.
