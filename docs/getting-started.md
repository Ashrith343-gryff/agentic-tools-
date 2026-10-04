# Getting Started

Welcome to the Agentic Tool Decider! This guide will walk you through setting up the project on your local machine.

## 1. Clone the Repository

First, download the code to your local machine:

```bash
git clone <your-repo-url>
cd agentic-tool-decider
```

## 2. Set Up Python

This project requires **Python 3.12**.

Create a virtual environment to isolate the project's dependencies:

```bash
python -m venv .venv
```

Activate the virtual environment:
- On Windows: `.venv\Scripts\activate`
- On macOS/Linux: `source .venv/bin/activate`

## 3. Install Dependencies

Currently, the core project uses standard library modules, but you might need `pytest` and `ruff` for testing and linting:

```bash
pip install pytest ruff
```

*(If a `requirements.txt` or `pyproject.toml` is present, install via `pip install -r requirements.txt` or `pip install -e .`)*

## 4. Run the Tests

Verify that everything is working correctly by running the test suite:

```bash
pytest
```

All tests should pass. The tests are designed to be fully deterministic and run offline.

## 5. Mock Mode vs. Jev Mode

The Tool Decider can operate in two primary modes:

### Mock Mode (Default / Offline)
By default, the decider runs in **Mock Mode** (`DECIDER_MODE=mock`). 
- **What it does:** Uses deterministic, local rules to select tools.
- **Why use it?** It requires **no network connection** and **no API keys**. It's perfect for local development, testing, and CI/CD.

### Jev Mode (Optional / Cloud)
If you want to use advanced LLM-based tool selection, you can use **Jev Mode** (`DECIDER_MODE=jev`).
- **What it does:** Calls the Jev AI API to evaluate and select the best tool.
- **Why use it?** Better handling of complex or ambiguous user queries.
- **Requirements:** You must have a Jev API key (`JEV_API_KEY`). See [docs/api-keys.md](api-keys.md) for how to get and use one securely.

## Next Steps

- Read through the [Architecture Guide](architecture.md) to understand how the components fit together.
- Check out `docs/api-keys.md` if you plan to use Jev Mode.
