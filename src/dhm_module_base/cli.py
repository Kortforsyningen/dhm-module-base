import logging
import click
from pkg_resources import iter_entry_points
from click_plugins import with_plugins
from dhm_module_base import __version__
from dhm_module_base import options
from dhm_module_base.helpers import (
    ClickColoredLoggingFormatter,
    ClickLoggingHandler,
)


def configure_logging(log_level):
    """Configure logging.

    Args:
        log_level (verbosity): Verbosity defines level of logging
    """
    handler = ClickLoggingHandler()
    handler.formatter = ClickColoredLoggingFormatter("%(name)s: %(message)s")
    logging.basicConfig(level=log_level.upper(), handlers=[handler])


@with_plugins(iter_entry_points("dhm_module_base.plugins"))
@click.group("dhm_module_base")
@click.version_option(version=__version__)
@options.verbosity_arg
def cli(verbosity):
    """dhm_module_base command line interface."""
    configure_logging(verbosity)
