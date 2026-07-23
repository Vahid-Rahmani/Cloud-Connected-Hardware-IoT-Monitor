"""Central configuration for the Cloud-Connected-Hardware-IoT-Monitor."""

import logging
import os

# ---------------------------------------------------------------------------
# 1. Master JSON schema definition
# ---------------------------------------------------------------------------
MONITOR_SCHEMA = {
    "type": "object",
    "required": ["agent_id", "timestamp", "metrics", "tags"],
    "properties": {
        "agent_id": {
            "type": "string",
            "description": "Unique identifier for the monitoring agent instance.",
        },
        "timestamp": {
            "type": "string",
            "format": "date-time",
            "description": "ISO-8601 timestamp of the reading.",
        },
        "metrics": {
            "type": "object",
            "required": ["total_gb", "used_gb", "free_gb", "usage_pct"],
            "properties": {
                "total_gb": {
                    "type": "number",
                    "description": "Total share capacity in gigabytes.",
                },
                "used_gb": {
                    "type": "number",
                    "description": "Used capacity in gigabytes.",
                },
                "free_gb": {
                    "type": "number",
                    "description": "Free capacity in gigabytes.",
                },
                "usage_pct": {
                    "type": "number",
                    "description": "Usage percentage (0.0 - 100.0).",
                },
            },
        },
        "tags": {
            "type": "object",
            "description": "Arbitrary key-value metadata (region, env, share name, etc.).",
            "additionalProperties": {"type": "string"},
        },
        "prefix_config": {
            "type": "object",
            "description": "Optional prefix/routing configuration for downstream consumers.",
            "properties": {
                "endpoint": {"type": "string"},
                "route_key": {"type": "string"},
            },
        },
        "suffix_status": {
            "type": "string",
            "enum": ["ok", "warning", "critical", "error"],
            "description": "Health-status suffix derived from threshold evaluation.",
        },
    },
}

# ---------------------------------------------------------------------------
# 2. Threshold constants
# ---------------------------------------------------------------------------
THRESHOLD_WARNING: float = 70.0
THRESHOLD_CRITICAL: float = 85.0

# ---------------------------------------------------------------------------
# 3. Azure / environment defaults
# ---------------------------------------------------------------------------
AZURE_STORAGE_ACCOUNT: str = os.getenv("AZURE_STORAGE_ACCOUNT", "")
AZURE_STORAGE_KEY: str = os.getenv("AZURE_STORAGE_KEY", "")
AZURE_FILE_SHARE_NAME: str = os.getenv("AZURE_FILE_SHARE_NAME", "")
POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))

# ---------------------------------------------------------------------------
# 4. Logging configuration
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"


def setup_logging() -> None:
    """Configure root logger for the application."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )
    # Quieten noisy third-party loggers
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
