import click
from pyfiglet import figlet_format

from tbx import cmds
from tbx.constants import CLI_NAME


@click.group(
    help=f"""\b
{figlet_format(CLI_NAME)}
{CLI_NAME} is a toolbox for the collection of various i/o operations built for my day-to-day needs.

Author: Rasheed Ibraheem 
"""
)
@click.version_option(message="%(package)s v%(version)s")
def cli() -> None:
    pass


cli.add_command(cmds.write_env)
cli.add_command(cmds.write_req)
