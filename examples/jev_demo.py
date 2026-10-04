"""
Jev demo for agentic-tool-decider.
"""

from decider.schema import JevRequest

from decider.config import DeciderConfig
from decider.jev_client import JevClient


def main() -> None:
    config = DeciderConfig()

    if not config.jev_api_key or config.jev_api_key == "NO_KEY":
        print("Jev mode requires a local key.")
        print("Please configure it by setting the JEV_API_KEY environment variable.")
        print("Example: export JEV_API_KEY=your_key_here")
        return

    print("Jev key found! Attempting to connect...")
    client = JevClient(api_key=config.jev_api_key, base_url=config.jev_base_url)

    try:
        response = client.send_request(JevRequest(prompt="Hello", candidates=[]))
        print(f"Jev response received: {response}")
    except Exception as e:
        print(f"Error calling Jev API: {e}")


if __name__ == "__main__":
    main()
