import logging
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Set gloabl environment path
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"

def actions() -> None:
    """Startup actions for the application."""
    load_dotenv(dotenv_path=ENV_PATH)
    
    logging.root.handlers.clear()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(ROOT_DIR / ".api.log")],
    )

    logger.info("Startup actions completed.")
