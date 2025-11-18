import argparse
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


def load_payload(payload_path: str = "payload.json") -> dict:
    """Load a JSON payload from a file."""
    if payload_path != "payload.json" and not verify_file_path(payload_path):
        raise FileNotFoundError(f"Payload file not found or not accessible: {payload_path}")
    
    logging.info(f"Loading payload from: {payload_path}")    
    with open(payload_path, encoding="utf-8") as f:
        return json.load(f)


def pretty_print(obj) -> None:
    """Pretty-print a JSON-serializable object."""
    print(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False))


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    This function sets up the argument parser and
    defines the command line arguments that can be used.

    :return: Parsed command line arguments.
    :rtype: argparse.Namespace
    """
    # Define the argument parser
    arg_parser = argparse.ArgumentParser(
        description=("SEKOIA API.\nSEKOIA API CLI Tool."),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Create a group for optional arguments
    group = arg_parser.add_argument_group(
        "Optional arguments", "Yippi yapp."
    )

    # Make a mutually exclusive group for schedule and export
    exclusive_group = group.add_mutually_exclusive_group()
    exclusive_group.add_argument(
        "-c",
        "--create",
        nargs="?",
        const="payload.json",
        metavar="PATH",
        help="Create an optimization rule from JSON payload. Default: ./payload.json",
    )
    exclusive_group.add_argument(
        "-d",
        "--delete",
        metavar="UUID",
        help="The rule UUID to delete",
    )
    exclusive_group.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all optimization rules",
    )
    
    logger.debug("Command line arguments parsed successfully.")
    return arg_parser.parse_args()


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