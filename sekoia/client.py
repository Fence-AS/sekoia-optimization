"""Sekoia.io Optimization Rules API client."""

import logging
from typing import Any

import requests
from dotenv import get_key

from utils.startup import ENV_PATH

logger = logging.getLogger(__name__)
BASE_URL = "https://api.sekoia.io"
BASE_PATH = "/v1/sic/conf/intakes/optimization_rules"


def api_request(
    session: requests.Session,
    method: str,
    endpoint: str | None = None,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    expected_status: int = 200,
) -> dict[str, Any] | None:
    """
    Run an API request and return the parsed response.

    :param session: The requests session.
    :type session: requests.Session
    :param method: HTTP method (GET, POST, etc.).
    :type method: str
    :param endpoint: API endpoint path, defaults to None.
    :type endpoint: str | None, optional
    :param params: HTTP query parameters, defaults to None.
    :type params: dict[str, Any] | None, optional
    :param json: JSON payload for the request, defaults to None.
    :type json: dict[str, Any] | None, optional
    :param expected_status: Expected HTTP status code(s), defaults to 200.
    :type expected_status: int, optional
    :raises SekoiaApiError: If the request fails (network error or unexpected HTTP status).
    :return: Parsed JSON response or None.
    :rtype: dict[str,Any] | None
    """
    # Send the request
    full_path = _url(endpoint)
    logger.info(f"Sending {method} API Request to {full_path}")
    try:
        response = session.request(
            method=method.upper(),
            url=full_path,
            params=params,
            json=json,
        )

        return _handle_response(response, expected_status)

    except requests.RequestException as error:
        logger.error(f"Network error contacting {full_path}: {error}")
        raise SekoiaApiError(f"Could not reach Sekoia API: {error}") from error

    except SekoiaApiError as error:
        logger.error(f"API request to {full_path} failed: {error}")
        raise


def get_session():
    """Verify API token and build a session."""
    api_token = get_key(ENV_PATH, "SEKOIA_API_TOKEN")
    if not api_token:
        raise SystemExit(
            "Please set the SEKOIA_API_TOKEN variable in the .env file before running."
        )

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


def _url(path: str | None = None) -> str:
    """Build the full URL from a path."""
    url = f"{BASE_URL}{BASE_PATH}"
    if path:
        url += f"{path}"

    return url


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
        raise SekoiaApiError(f"Request failed with status {response.status_code}: {detail}")

    logger.info(f"Request received with status {response.status_code}")

    if response.status_code == 204:
        return None

    if response.headers.get("Content-Type", "").startswith("application/json"):
        return response.json()

    return response.text


class SekoiaApiError(Exception):
    """Raised when the Sekoia API returns a non-success status code."""
