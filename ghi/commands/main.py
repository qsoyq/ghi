import logging

import typer

import ghi.commands.release
from ghi.utils import is_cmd_exists
from ghi.utils import error
from ghi.utils import version_callback
from ghi.settings import settings

helptext = """
A wrapper for github cli.

https://cli.github.com/
"""

cmd = typer.Typer(help=helptext)
cmd.add_typer(ghi.commands.release.cmd, name="release")


@cmd.callback(invoke_without_command=True)
def default(
    log_level: int = typer.Option(settings.log.log_level, "--log_level", envvar="log_level", help="日志级别, DEBUG:10, INFO: 20, WARNING: 30, ERROR:40"),
    log_format: str = typer.Option(settings.log.log_format),
    _: bool = typer.Option(False, "--version", "-V", "-v", callback=version_callback),
):
    logging.basicConfig(level=log_level, format=log_format)
    if not is_cmd_exists("gh"):
        typer.echo(error("gh not found"))
        raise typer.Exit(-1)


if __name__ == "__main__":
    cmd()
