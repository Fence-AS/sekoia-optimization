"""Startup actions for the Sekoia.io Optimization Rules tool."""

import logging
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Set global environment path
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
LOG_FILE = ROOT_DIR / ".api.log"
MAX_LOG_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def actions() -> None:
    """Startup actions for the application."""
    load_dotenv(dotenv_path=ENV_PATH)

    log_rotated = False
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > MAX_LOG_SIZE_BYTES:
        LOG_FILE.unlink()
        log_rotated = True

    logging.root.handlers.clear()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(LOG_FILE)],
    )

    if log_rotated:
        logger.info("Log file rotated due to size limit.")

    logger.info("Startup actions completed.")
