import click
from dhm_module_base.settings import Configuration

CONFIG = Configuration().config
LOG_LEVEL = CONFIG["DEFAULT"]["loglevel"]

# pylint: disable=invalid-name
verbosity_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
verbosity_arg = click.option(
    "--verbosity",
    "-v",
    # pylint: disable=unexpected-keyword-arg
    type=click.Choice(choices=verbosity_levels, case_sensitive=False),
    default=LOG_LEVEL,
    help="Set verbosity level",
)
