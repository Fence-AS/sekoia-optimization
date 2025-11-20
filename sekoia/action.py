"""Sekoia.io optimization rules API actions."""
import logging
from typing import Any

import requests

from sekoia import client
from utils import helpers

logger = logging.getLogger(__name__)


def list_optimization_rules(
    session: requests.Session,
    *,
    community_uuid: str | None = None,
    intake_uuid: str | None = None,
    agent_id: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any] | None:
    """
    List SEKOIA Optimization rules.

    :param session: The requests session.
    :type session: requests.Session
    :param community_uuid: Community UUID, defaults to None
    :type community_uuid: str | None, optional
    :param intake_uuid: Intake UUID, defaults to None
    :type intake_uuid: str | None, optional
    :param agent_id: Agent ID, defaults to None
    :type agent_id: str | None, optional
    :param limit: Results page limit, defaults to 20
    :type limit: int, optional
    :param offset: Offsett results page, defaults to 0
    :type offset: int, optional
    :return: List of optimization rules.
    :rtype: dict[str, Any]
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
    
    response = client.api_request(
        session=session,
        method="GET",
        params=params,
    )
    
    if response:
        print("List Optimization Rules\n------------------------------")
        helpers.pretty_print(response)
        
        return response


def create_optimization_rule(
    session: requests.Session,
    rule: dict[str, Any],
) -> dict[str, Any] | None:
    """
    Create a SEKOIA Optimization rules.

    :param session: The requests session.
    :type session: requests.Session
    :param rule: The optimization rule payload to create.
    :type rule: dict[str, Any]
    :return: Created optimization rule.
    :rtype: dict[str, Any]
    """     
    response = client.api_request(
        session=session,
        method="POST",
        json=rule,
    )
    
    if response:
        return response


def list_optimization_actions(session: requests.Session) -> dict[str, Any] | None:
    """
    List supported for Optimization rule actions.

    :param session: The requests session.
    :type session: requests.Session
    :return: List of supported optimization rule actions.
    :rtype: dict[str, Any]
    """   
    response = client.api_request(
        session=session,
        method="GET",
        endpoint="/actions",
    )
    
    if response:
        print("List Supported Optimization Actions\n------------------------------")
        helpers.pretty_print(response)
        
        return response


def get_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> dict[str, Any] | None:
    """
    Get a SEKOIA Optimization rule.

    :param session: The requests session.
    :type session: requests.Session
    :param uuid: The optimization rule UUID.
    :type uuid: str
    :return: Optimization rule details.
    :rtype: dict[str, Any]
    """
    response = client.api_request(
        session=session,
        method="GET",
        endpoint=f"/{uuid}",
    )
    
    if response:
        return response


def delete_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Delete a SEKOIA Optimization rule.

    :param session: The requests session.
    :type session: requests.Session
    :param uuid: The optimization rule UUID.
    :type uuid: str
    """
    client.api_request(
        session=session,
        method="DELETE",
        endpoint=f"/{uuid}",
        expected_status=204,
    )
    
    
def disable_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Disable a SEKOIA Optimization rules.

    :param session: The requests session.
    :type session: requests.Session
    :param uuid: The optimization rule UUID.
    :type uuid: str
    """
    client.api_request(
        session=session,
        method="POST",
        endpoint=f"/{uuid}/disable",
        expected_status=204,
    )
    
    
def enable_optimization_rule(
    session: requests.Session,
    uuid: str,
) -> None:
    """
    Enable a SEKOIA Optimization rules.

    :param session: The requests session.
    :type session: requests.Session
    :param uuid: The optimization rule UUID.
    :type uuid: str
    """
    client.api_request(
        session=session,
        method="POST",
        endpoint=f"/{uuid}/enable",
        expected_status=204,
    )
    