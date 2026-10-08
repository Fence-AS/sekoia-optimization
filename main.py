"""Main module for Sekoia.io optimization rules management."""

import logging

from sekoia.client import get_session
from utils import cli, startup

logger = logging.getLogger(__name__)


def main() -> None:
    """Entry point for the Sekoia API."""
    startup.actions()

    args = cli.parse_cli_args()

    # No action flags at all -> enter interactive mode instead of exiting.
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
        session = get_session()
        cli.run_interactive(session)
        return

    # Perform actions based on argument
    session = get_session()
    cli.handle_arguments(args, session)


if __name__ == "__main__":
    main()
