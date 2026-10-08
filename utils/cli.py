"""CLI logic for Sekoia.io Optimization Rules tool."""

import argparse
import logging

from sekoia import action
from utils import helpers

logger = logging.getLogger(__name__)


def _prompt_uuid() -> str:
    return input("Rule UUID: ").strip()


_MENU_ACTIONS = {
    "1": ("list", lambda: True),
    "2": ("create", lambda: input("Payload path [payload.json]: ").strip() or "payload.json"),
    "3": ("actions", lambda: True),
    "4": ("get", _prompt_uuid),
    "5": ("remove", _prompt_uuid),
    "6": ("disable", _prompt_uuid),
    "7": ("enable", _prompt_uuid),
}

_MENU_TEXT = """
Sekoia Optimization Rules - Interactive Mode
  1) List optimization rules
  2) Create optimization rule
  3) List supported actions
  4) Get a rule
  5) Remove a rule
  6) Disable a rule
  7) Enable a rule
  q) Quit
"""


def build_parser() -> argparse.ArgumentParser:
    """
    Build the CLI argument parser.

    Factored out of `parse_cli_args` so interactive mode can seed a
    fully-defaulted `argparse.Namespace` from the same definitions.

    :return: The configured argument parser.
    :rtype: argparse.ArgumentParser
    """
    arg_parser = argparse.ArgumentParser(
        description=(
            "Sekoia.io Optimization Rules.\n"
            "A CLI tool to simplify the management of Optimization Rules in the Sekoia API."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Create a group for optional arguments
    group = arg_parser.add_argument_group(
        "Arguments", "Mutually exclusive arguments reflecting Sekoia's API Scheme."
    )

    # Make a mutually exclusive group for schedule and export
    exclusive_group = group.add_mutually_exclusive_group()
    exclusive_group.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all optimization rules",
    )
    exclusive_group.add_argument(
        "-c",
        "--create",
        nargs="?",
        const="payload.json",
        metavar="PATH",
        help="Create an optimization rule from JSON payload. Default: ./payload.json",
    )
    exclusive_group.add_argument(
        "-a",
        "--actions",
        action="store_true",
        help="List all supported optimization actions",
    )
    exclusive_group.add_argument(
        "-g",
        "--get",
        metavar="UUID",
        help="Get the given rule UUID",
    )
    exclusive_group.add_argument(
        "-r",
        "--remove",
        metavar="UUID",
        help="Remove the given rule UUID",
    )
    exclusive_group.add_argument(
        "-d",
        "--disable",
        metavar="UUID",
        help="Disable the given rule UUID",
    )
    exclusive_group.add_argument(
        "-e",
        "--enable",
        metavar="UUID",
        help="Enable the given rule UUID",
    )

    list_group = arg_parser.add_argument_group("List options", "Only apply with --list.")
    list_group.add_argument("--community", metavar="UUID", help="Filter by community UUID")
    list_group.add_argument("--intake", metavar="UUID", help="Filter by intake UUID")
    list_group.add_argument("--agent", metavar="UUID", help="Filter by agent ID")
    list_group.add_argument(
        "--limit", type=int, default=100, metavar="N", help="Page limit (default: 100)"
    )
    list_group.add_argument(
        "--offset", type=int, default=0, metavar="N", help="Page offset (default: 0)"
    )

    arg_parser.add_argument(
        "--raw", action="store_true", help="Print raw JSON instead of formatted text."
    )
    arg_parser.add_argument(
        "-y", "--yes", action="store_true", help="Skip y/N confirmation prompts."
    )

    return arg_parser


def parse_cli_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    :return: Parsed command line arguments.
    :rtype: argparse.Namespace
    """
    args = build_parser().parse_args()
    logger.info("Command line arguments parsed.")
    return args


def _confirmed(args, message: str) -> bool:
    """Ask for y/N confirmation, unless --yes was passed."""
    if args.yes:
        return True
    if input(f"{message} (y/N): ").strip().lower() == "y":
        return True
    print("Operation cancelled by user.")
    return False


def _report_error(error: Exception) -> None:
    """Log full detail to file and print a clean one-line message to console."""
    logger.error(str(error), exc_info=True)
    print(f"Error: {error}")


def _dispatch(args, session) -> None:
    """Run the action selected by args.

    Raises on failure, callers decide what to do with it (exit the process
    for one-shot use, or log and keep looping for interactive mode).

    :param args: Arguments from command line (or a seeded interactive Namespace).
    :type args: _argparse.Namespace_
    :param session: The requests session.
    :type session: _requests.Session_
    """
    if args.list:
        logger.info("Listing optimization rules.")
        rules = action.list_optimization_rules(
            session=session,
            community_uuid=args.community,
            intake_uuid=args.intake,
            agent_id=args.agent,
            limit=args.limit,
            offset=args.offset,
        )
        print("List Optimization Rules\n------------------------------")
        helpers.print_rule_list(rules, raw=args.raw)

    elif args.create:
        logger.info("Creating an optimization rule.")
        payload = helpers.load_payload(args.create)
        print("Optimization Rule Payload:\n------------------------------")
        helpers.print_rule(payload, raw=args.raw)

        if not _confirmed(args, "Are you sure you want to create this optimization rule?"):
            return
        print("---")
        helpers.print_rule(
            action.create_optimization_rule(session=session, rule=payload), raw=args.raw
        )

    elif args.actions:
        logger.info("Listing supported optimization rule actions.")
        print("List Supported Optimization Actions\n------------------------------")
        helpers.print_actions(action.list_optimization_actions(session=session), raw=args.raw)

    elif args.get:
        logger.info(f"Getting optimization rule with UUID: {args.get}")
        rule = action.get_optimization_rule(session=session, uuid=args.get)
        print("Optimization Rule Details\n------------------------------")
        helpers.print_rule(rule, raw=args.raw)

    elif args.remove:
        logger.info(f"Removing optimization rule with UUID: {args.remove}")

        if not _confirmed(
            args, f"Are you sure you want to remove the optimization rule {args.remove}?"
        ):
            return

        action.delete_optimization_rule(session=session, uuid=args.remove)
        print(f"Optimization rule {args.remove} has been deleted.")

    elif args.disable:
        logger.info(f"Disabling optimization rule with UUID: {args.disable}")

        if not _confirmed(
            args, f"Are you sure you want to disable the optimization rule {args.disable}?"
        ):
            return

        action.disable_optimization_rule(session=session, uuid=args.disable)
        print(f"Optimization rule {args.disable} has been disabled.")

    elif args.enable:
        logger.info(f"Enabling optimization rule with UUID: {args.enable}")

        if not _confirmed(
            args, f"Are you sure you want to enable the optimization rule {args.enable}?"
        ):
            return

        action.enable_optimization_rule(session=session, uuid=args.enable)
        print(f"Optimization rule {args.enable} has been enabled.")


def handle_arguments(args, session) -> None:
    """One-shot CLI entry point: dispatch, and exit the process on any failure.

    :param args: Arguments from command line.
    :type args: _argparse.Namespace_
    :param session: The requests session.
    :type session: _requests.Session_
    """
    try:
        _dispatch(args, session)
    except Exception as error:
        _report_error(error)
        raise SystemExit(1) from None


def run_interactive(session) -> None:
    """Menu-driven loop for interactive mode.

    Reuses `_dispatch` so the actual command logic is defined in exactly one
    place, only the error-handling policy differs from `handle_arguments`
    (log and keep looping here, instead of exiting the process).

    :param session: The requests session.
    :type session: _requests.Session_
    """
    parser = build_parser()
    print(_MENU_TEXT)
    try:
        while True:
            choice = input("Choice (m for menu): ").strip().lower()
            if choice in ("q", "quit", "exit"):
                return
            if choice == "m":
                print(_MENU_TEXT)
                continue
            if choice not in _MENU_ACTIONS:
                print("Unknown choice. Enter a number 1-7, m, or q.")
                continue

            attr, prompt = _MENU_ACTIONS[choice]
            args = parser.parse_args([])
            setattr(args, attr, prompt())

            try:
                _dispatch(args, session)
            except Exception as error:
                _report_error(error)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
