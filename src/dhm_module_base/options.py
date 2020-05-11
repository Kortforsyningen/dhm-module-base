import click

# pylint: disable=invalid-name
verbosity_levels = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
verbosity_arg = click.option(
    "--verbosity",
    "-v",
    # pylint: disable=unexpected-keyword-arg
    type=click.Choice(choices=verbosity_levels, case_sensitive=False),
    default="ERROR",
    help="Set verbosity level",
)
