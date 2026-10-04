import os
from dataclasses import dataclass


@dataclass
class Settings:
    decider_mode: str = "mock"
    jev_api_key: str = ""
    jev_api_base_url: str = "https://www.jevai.org"
    decision_confidence_threshold: float = 0.80

    def diagnostics(self) -> dict[str, str]:
        return {
            "decider_mode": self.decider_mode,
            "jev_api_key": "configured" if self.jev_api_key else "not configured",
            "jev_api_base_url": self.jev_api_base_url,
            "decision_confidence_threshold": str(self.decision_confidence_threshold),
        }


def load_settings() -> Settings:
    mode = os.getenv("DECIDER_MODE", "mock")
    api_key = os.getenv("JEV_API_KEY", "")
    base_url = os.getenv("JEV_API_BASE_URL", "https://www.jevai.org")

    threshold_str = os.getenv("DECISION_CONFIDENCE_THRESHOLD", "0.80")
    try:
        threshold = float(threshold_str)
    except ValueError:
        threshold = 0.80

    return Settings(
        decider_mode=mode,
        jev_api_key=api_key,
        jev_api_base_url=base_url,
        decision_confidence_threshold=threshold,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "check":
        settings = load_settings()
        diag = settings.diagnostics()
        print("Decider Configuration Diagnostics:")
        for k, v in diag.items():
            print(f"  {k}: {v}")
