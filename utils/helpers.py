"""Helper functions for Sekoia.io Optimization Rules tool."""
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def load_payload(payload_path: str = "payload.json") -> dict:
    """
    Load a JSON payload from a file.

    :param payload_path: The path to the JSON payload file, defaults to "payload.json".
    :type payload_path: str, optional
    :raises FileNotFoundError: If the file does not exist or is not accessible.
    :return: The loaded JSON payload.
    :rtype: dict
    """
    if payload_path != "payload.json" and not verify_file_path(payload_path):
        raise FileNotFoundError(f"Payload file not found or not accessible: {payload_path}")
    
    logging.info(f"Loading payload from: {payload_path}")    
    with open(payload_path, encoding="utf-8") as f:
        return json.load(f)


def pretty_print(obj) -> None:
    """
    Pretty-print a JSON-serializable object.

    :param obj: The object to pretty-print.
    :type obj: _any_
    """
    print(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False))


def verify_file_path(file_path: str) -> bool:
    """
    Verify the given file path as writeable and accessable.

    :param path: The file path to verify
    :type path: str
    :return: The stauts of the verification
    :rtype: bool
    """
    try:
        path = Path(file_path).expanduser().resolve()
        folder = path.parent
        
        if not folder.is_dir():
            logger.warning("Log path parent is not an existing directory.")
            return False

        if not os.access(folder, os.W_OK):
            logger.warning("Log path parent is not writeable.")
            return False

        if path.is_dir():
            logger.warning("Log path must be a file.")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to verify given file path with error: {e}")
        return False