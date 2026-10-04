import json
import urllib.error
import urllib.request
from typing import Any


class JevClient:
    """HTTP client for the Jev REST API.

    Handles authentication, network requests, timeouts, and error handling.
    Does not contain tool-ranking business logic.
    """

    def __init__(self, api_key: str, base_url: str = "https://www.jevai.org", timeout: int = 10):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def post_decision(self, endpoint_path: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Send a POST request to a Jev decision endpoint.

        Args:
            endpoint_path: The API path, e.g., '/api/v1/decisions'.
            payload: The JSON-serializable request payload.

        Returns:
            The parsed JSON response.

        Raises:
            RuntimeError: On connection errors, timeouts, or API-level errors.
        """
        url = f"{self.base_url}{endpoint_path}"
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                if result.get("code") != 0:
                    msg = result.get("message", "Unknown error")
                    raise RuntimeError(f"Jev API error: {msg}")
                return result
        except urllib.error.HTTPError as e:
            # Read error body if available
            try:
                error_body = json.loads(e.read().decode("utf-8"))
                msg = error_body.get("message", e.reason)
            except Exception:
                msg = e.reason
            raise RuntimeError(f"Jev API HTTP {e.code}: {msg}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Jev API connection error: {e.reason}")
        except TimeoutError:
            raise RuntimeError("Jev API request timed out")
