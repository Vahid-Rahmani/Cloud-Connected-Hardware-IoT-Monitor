"""Cloud-Connected-Hardware-IoT-Monitor – application entry point."""

import json
import logging
import os

from monitor.config import setup_logging

logger = logging.getLogger(__name__)


def run() -> None:
    """Main application entry point."""
    setup_logging()
    logger.info("Cloud-Connected-Hardware-IoT-Monitor starting up")
    logger.debug(
        "Environment: AZURE_STORAGE_ACCOUNT=%s, POLL_INTERVAL_SECONDS=%s",
        os.getenv("AZURE_STORAGE_ACCOUNT", "(not set)"),
        os.getenv("POLL_INTERVAL_SECONDS", "300"),
    )


if __name__ == "__main__":
    run()
