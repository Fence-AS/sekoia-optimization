"""Main module for Sekoia.io optimization rules management."""
import logging

from sekoia.client import get_session
from utils import cli, startup

logger = logging.getLogger(__name__)
        

def main() -> None:
    """Entry point for the Sekoia API."""
    startup.actions()

    args = cli.parse_cli_args()

    # Explicitly check the mutually exclusive actions
    if not any(
        (
            args.list,
            args.create,
            args.actions,
            args.get,
            args.remove,
            args.disable,
            args.enable,
        )
    ):
        print("No action provided. Use -h for help.")
        return

    # Preform actions based on argument
    session = get_session()
    cli.handle_agruments(args, session)


if __name__ == "__main__":
    main()
    