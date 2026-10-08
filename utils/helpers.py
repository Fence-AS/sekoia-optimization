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


def print_rule(rule: dict, raw: bool = False) -> None:
    """Print a single rule (used for --get, and both the --create preview and result)."""
    print(_dump(rule) if raw else format_rule(rule))


def print_rule_list(payload: dict, raw: bool = False) -> None:
    """Print a {"items": [...], "total": N} list-of-rules response."""
    print(_dump(payload) if raw else format_rule_list(payload))


def print_actions(payload: dict, raw: bool = False) -> None:
    """Print a {"actions": [...]} response."""
    print(_dump(payload) if raw else format_actions(payload))


def _dump(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


def format_rule(rule: dict) -> str:
    """Render a rule as a labeled detail block.

    Fields: uuid/intake_uuid/format_uuid/community_uuid/agent_id/filters/
    action/description/enabled/created_*/updated_*.
    """
    lines = []
    if rule.get("uuid"):
        lines.append(f"UUID:         {rule['uuid']}")
    lines.append(f"Description:  {rule.get('description') or '(none)'}")
    lines.append(f"Enabled:      {_yes_no(rule)}")
    lines.append(f"Action:       {rule.get('action', '')}")

    for key, label in (
        ("community_uuid", "Community"),
        ("intake_uuid", "Intake"),
        ("format_uuid", "Format"),
        ("agent_id", "Agent"),
    ):
        if rule.get(key):
            lines.append(f"{label + ':':<14}{rule[key]}")

    filters = rule.get("filters") or []
    if filters:
        lines.append("Filters:")
        lines.extend(f"  - {_format_filter(f)}" for f in filters)

    for prefix, label in (("created", "Created"), ("updated", "Updated")):
        if rule.get(f"{prefix}_at"):
            lines.append(
                f"{label + ':':<14}{rule[f'{prefix}_at']} by {rule.get(f'{prefix}_by', '?')} "
                f"({rule.get(f'{prefix}_by_type', '?')})"
            )
    return "\n".join(lines)


def _yes_no(rule: dict) -> str:
    return "yes" if rule.get("enabled", True) else "no"


def _format_filter(f: dict) -> str:
    parts = [f.get("field", ""), f.get("operator", "")]
    if "value" in f:
        parts.append(_format_value(f["value"]))
    return " ".join(parts)


def _format_value(value) -> str:
    return f'"{value}"' if isinstance(value, str) else str(value)


def format_rule_list(payload: dict) -> str:
    """Render a {"items": [...], "total": N} response as a UUID/ENABLED/ACTION/DESCRIPTION table."""
    items = payload.get("items", [])
    total = payload.get("total", len(items))
    if not items:
        return "No rules found."

    headers = ("UUID", "ENABLED", "ACTION", "DESCRIPTION")
    rows = [_rule_row(rule) for rule in items]
    return _table(headers, rows) + f"\n\nShowing {len(items)} of {total} rule(s)."


def _rule_row(rule: dict) -> tuple[str, str, str, str]:
    return (
        rule.get("uuid", ""),
        _yes_no(rule),
        str(rule.get("action", "")),
        rule.get("description") or "",
    )


def format_actions(payload: dict) -> str:
    """Render a {"actions": [{action, name, description}, ...]} response as a table."""
    actions = payload.get("actions", [])
    if not actions:
        return "No actions found."
    headers = ("VALUE", "NAME", "DESCRIPTION")
    rows = [_action_row(a) for a in actions]
    return _table(headers, rows)


def _action_row(a: dict) -> tuple[str, str, str]:
    return (str(a.get("action", "")), a.get("name", ""), a.get("description", ""))


def _table(headers: tuple, rows: list[tuple]) -> str:
    widths = [max(len(h), max((len(r[i]) for r in rows), default=0)) for i, h in enumerate(headers)]

    def line(row):
        return "  ".join(cell.ljust(w) for cell, w in zip(row, widths, strict=True))

    return "\n".join([line(headers), line(["-" * w for w in widths]), *[line(r) for r in rows]])


def verify_file_path(file_path: str) -> bool:
    """
    Verify the given file path as writeable and accessible.

    :param file_path: The file path to verify
    :type file_path: str
    :return: The status of the verification
    :rtype: bool
    """
    try:
        path = Path(file_path).expanduser().resolve()
        folder = path.parent

        if not folder.is_dir():
            logger.warning("Path parent is not an existing directory.")
            return False

        if not os.access(folder, os.W_OK):
            logger.warning("Path parent is not writeable.")
            return False

        if path.is_dir():
            logger.warning("Path must be a file, not a directory.")
            return False

        return True

    except Exception as e:
        logger.error(f"Failed to verify given file path with error: {e}")
        return False
