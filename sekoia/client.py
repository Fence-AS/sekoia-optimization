import logging
from typing import Any

import requests
from dotenv import get_key

from utils.startup import ENV_PATH

logger = logging.getLogger(__name__)
BASE_URL = "https://api.sekoia.io"


def get_session():
    """Verify API token and build a session."""
    api_token = get_key(ENV_PATH, "SEKOIA_API_TOKEN")
    if not api_token:
        raise SystemExit("Please set the SEKOIA_API_TOKEN variable in the .env file before running.")
    
    return build_session(api_token)
    

def build_session(api_token: str) -> requests.Session:
    """
    Create a configured requests.Session with Authorization headers set.

    Assumes a Bearer-style token in the Authorization header, which is how
    Sekoia's API is typically used.
    """
    if not api_token:
        raise ValueError("API token is empty. Please set API_TOKEN.")

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
        }
    )
    
    logger.info("Session created with Authorization header set.")
    return session


def _url(path: str) -> str:
    """Build the full URL from a path."""
    return f"{BASE_URL}{path}"


def _handle_response(
    response: requests.Response,
    expected_status: int | tuple[int, ...] = (200,),
) -> Any:
    """
    Validate response status and return parsed JSON (if any).

    Raises SekoiaApiError on unexpected status codes.
    """
    if isinstance(expected_status, int):
        expected_status = (expected_status,)

    if response.status_code not in expected_status:
        try:
            detail = response.json()
        except Exception:
            detail = response.text
        raise SekoiaApiError(
            f"Request failed with status {response.status_code}: {detail}"
        )

    logger.info(f"Request recieved with status {response.status_code}")

    if response.status_code == 204:
        return None

    if response.headers.get("Content-Type", "").startswith("application/json"):
        return response.json()

    return response.text

class SekoiaApiError(Exception):
    """Raised when the Sekoia API returns a non-success status code."""

