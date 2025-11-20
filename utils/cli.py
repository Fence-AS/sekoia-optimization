"""CLI logic for Sekoia.io Optimization Rules tool."""
import argparse
import logging

from sekoia import action
from utils import helpers

logger = logging.getLogger(__name__)


def parse_cli_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    This function sets up the argument parser and
    defines the command line arguments that can be used.

    :return: Parsed command line arguments.
    :rtype: argparse.Namespace
    """
    # Define the argument parser
    arg_parser = argparse.ArgumentParser(
        description=(
            "Sekoia.io Optimization Rules.\n"
            "A CLI tool to simplify the management of Optimization Rules in the Sekoia API."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Create a group for optional arguments
    group = arg_parser.add_argument_group(
        "Arguments", 
        "Mutually exclusive arguments reflecting Sekoia's API Scheme."
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
        
    logger.info("Command line arguments parsed.")
    return arg_parser.parse_args()

def handle_agruments(args, session) -> None:
    """Handle arguments given from command line.

    :param args: Arguments from command line.
    :type args: _argparse.Namespace_
    :param session: The requests session.
    :type session: _requests.Session_
    """
    if args.list:
        logger.info("Listing optimization rules.")
        action.list_optimization_rules(session=session)
    
    elif args.create:
        logger.info("Creating an optimization rule.")
        payload = helpers.load_payload(args.create)
        print("Optimization Rule Payload:\n------------------------------")
        helpers.pretty_print(payload)
        
        confirm = input(
            "Are you sure you want to create this optimization rule? (y/N): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled by user.")
            return
        print("---")
        helpers.pretty_print(
            action.create_optimization_rule(session=session, rule=payload)
        )
        
    elif args.actions:
        logger.info("Listing supported optimization rule actions.")
        action.list_optimization_actions(session=session)
    
    elif args.get:
        logger.info(f"Getting optimization rule with UUID: {args.get}")
        rule = action.get_optimization_rule(session=session, uuid=args.get)
        if rule:
            print("Optimization Rule Details\n------------------------------")
            helpers.pretty_print(rule)
    
    elif args.remove:
        logger.info(f"Removing optimization rule with UUID: {args.remove}")
        
        confirm = input(
            f"Are you sure you want to delete/remove the optimization rule {args.remove}? (y/N): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled by user.")
            return
        
        action.delete_optimization_rule(session=session, uuid=args.remove)
        print(f"Optimization rule {args.remove} has been deleted.")
    
    elif args.disable:
        logger.info(f"Disabling optimization rule with UUID: {args.disable}")
        
        confirm = input(
            f"Are you sure you want to disable the optimization rule {args.disable}? (y/N): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled by user.")
            return
        
        action.disable_optimization_rule(session=session, uuid=args.disable)
        print(f"Optimization rule {args.disable} has been disabled.")
    
    elif args.enable:
        logger.info(f"Enabling optimization rule with UUID: {args.enable}")
        
        confirm = input(
            f"Are you sure you want to enable the optimization rule {args.enable}? (y/N): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled by user.")
            return
        
        action.enable_optimization_rule(session=session, uuid=args.enable)
        print(f"Optimization rule {args.enable} has been enabled.")