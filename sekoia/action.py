"""Sekoia.io optimization rules API actions."""
import logging
from typing import Any

import requests

import utils.helpers
from sekoia import client

logger = logging.getLogger(__name__)


def list_optimization_rules(
    session: requests.Session,
    *,
    community_uuid: str | None = None,
    intake_uuid: str | None = None,
    agent_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """
    List Optimization rules.

    GET /v1/sic/conf/intakes/optimization_rules

    Optional filters:
      - community_uuid -> match[community_uuid]
      - intake_uuid    -> match[intake_uuid]
      - agent_id       -> match[agent_id]
      - limit/offset   for pagination
    """
    params: dict[str, Any] = {
        "limit": limit,
        "offset": offset,
    }

    if community_uuid:
        params["match[community_uuid]"] = community_uuid
    if intake_uuid:
        params["match[intake_uuid]"] = intake_uuid
    if agent_id:
        params["match[agent_id]"] = agent_id

    resp = session.get(client._url("/v1/sic/conf/intakes/optimization_rules"), params=params)
    resp_text = client._handle_response(resp, expected_status=200)
    
    print("List Optimization Rules\n------------------------------")
    utils.helpers.pretty_print(resp_text)
    
    return resp_text


def create_optimization_rule(
    session: requests.Session,
    rule: dict[str, Any],
) -> dict[str, Any]:
    """
    Create a new optimization rule.

    POST /v1/sic/conf/intakes/optimization_rules 

    The schema in the OpenAPI file leaves 'properties' empty, so this function
    accepts an arbitrary JSON object. It’s up to the caller to pass a
    payload matching what your Sekoia instance expects.
    """
    resp = session.post(
        client._url("/v1/sic/conf/intakes/optimization_rules"),
        json=rule,
    )
    
    # According to schema: 200 on success 
    return client._handle_response(resp, expected_status=200)


def list_optimization_actions(session: requests.Session) -> dict[str, Any]:
    """
    List Actions supported for Optimization rules.

    GET /v1/sic/conf/intakes/optimization_rules/actions
    """
    resp = session.get(client._url("/v1/sic/conf/intakes/optimization_rules/actions"))
    return client._handle_response(resp, expected_status=200)


def get_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> dict[str, Any]:
    """
    Get an Optimization rule by UUID.

    GET /v1/sic/conf/intakes/optimization_rules/{uuid}
    """
    resp = session.get(
        client._url(f"/v1/sic/conf/intakes/optimization_rules/{uuid}")
    )
    return client._handle_response(resp, expected_status=200)


def delete_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Delete an Optimization rule.

    DELETE /v1/sic/conf/intakes/optimization_rules/{uuid}

    Returns None on success (204).
    """
    resp = session.delete(
        client._url(f"/v1/sic/conf/intakes/optimization_rules/{uuid}")
    )
    client._handle_response(resp, expected_status=204)
    
    
def disable_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Disable an Optimization rule.

    POST /v1/sic/conf/intakes/optimization_rules/{uuid}/disable

    Returns None on success (204).
    """
    resp = session.post(
        client._url(f"/v1/sic/conf/intakes/optimization_rules/{uuid}/disable")
    )
    client._handle_response(resp, expected_status=204)
    
    
def enable_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Enable an Optimization rule.

    POST /v1/sic/conf/intakes/optimization_rules/{uuid}/enable

    Returns None on success (204).
    """
    resp = session.post(
        client._url(f"/v1/sic/conf/intakes/optimization_rules/{uuid}/enable")
    )
    client._handle_response(resp, expected_status=204)
    
    