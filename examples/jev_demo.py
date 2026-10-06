"""
Jev decision backend demo for agentic-tool-decider.
"""

import os
from decider.config import Settings, load_settings
from decider.jev_client import JevClient
from decider.jev_selector import JevSelector
from decider.models import ToolCandidate


def main() -> None:
    settings = load_settings()

    if not settings.jev_api_key or settings.jev_api_key.strip() == "":
        print("Notice: Jev API Key is not configured.")
        print("To run this demo with the real Jev AI backend, please:")
        print("1. Get a key from https://www.jevai.org")
        print("2. Set JEV_API_KEY as an environment variable or in your .env file.")
        print("\nDiagnostics:")
        for k, v in settings.diagnostics().items():
            print(f"  {k}: {v}")
        return

    print("Jev API Key found. Initializing Jev integration...\n")
    
    client = JevClient(api_key=settings.jev_api_key, base_url=settings.jev_api_base_url)
    selector = JevSelector(client=client)

    candidates = [
        ToolCandidate(
            name="calculator",
            description="Performs arithmetic calculations such as addition, subtraction, multiplication, and division",
            input_schema={},
        ),
        ToolCandidate(
            name="search_knowledge",
            description="Searches a local knowledge base of workshop documents using semantic retrieval",
            input_schema={},
        )
    ]

    request = "What is 120 / 4?"
    print(f"Request: {request}")
    print("Asking Jev...\n")
    
    try:
        decision = selector.select(request, candidates)
        print("Jev Decision:")
        print(f"  Decision Type: {decision.decision}")
        print(f"  Selected Tool: {decision.tool}")
        print(f"  Confidence: {decision.confidence}")
        print(f"  Reason: {decision.reason}")
    except Exception as e:
        print(f"Error querying Jev API: {e}")


if __name__ == "__main__":
    main()
