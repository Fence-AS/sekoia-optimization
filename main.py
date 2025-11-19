"""Main module for Sekoia.io optimization rules management."""
import logging
from pathlib import Path

from sekoia import action
from sekoia.client import get_session
from utils import helpers, startup

logger = logging.getLogger(__name__)

def agruments(args, session) -> None:
    """Handle arguments given from command line.

    :param args: Arguments from command line.
    :type args: _argparse.Namespace_
    :param session: The requests session.
    :type session: _requests.Session_
    """
    if args.list:
        logger.info("Listing optimization rules.")
        action.list_optimization_rules(session=session)
    
    if args.create:
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
    if args.delete:
        logger.info(f"Deleting optimization rule with UUID: {args.delete}")
        
        confirm = input(
            f"Are you sure you want to delete the optimization rule {args.delete}? (y/N): "
        )
        if confirm.lower() != "y":
            print("Operation cancelled by user.")
            return
        
        action.delete_optimization_rule(session=session, uuid=args.delete)
        print(f"Optimization rule {args.delete} has been deleted.")
        
    if args.actions:
        logger.info("Listing supported optimization rule actions.")
        action.list_optimization_actions(session=session)
        
    

def main() -> None:
    """Entry point for the Sekoia API."""
    startup.actions()
    
    session = get_session()
    
    args_given = helpers.parse_args()   
    if any(vars(args_given).values()):
        agruments(args_given, session)


if __name__ == "__main__":
    main()
    