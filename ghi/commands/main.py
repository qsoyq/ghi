import typer

import ghi.commands.release
from ghi.commands import default_invoke_without_command

helptext = """
A wrapper for github cli.

https://cli.github.com/
"""

cmd = typer.Typer(help=helptext)
cmd.add_typer(ghi.commands.release.cmd, name="release")


def add_default_invoke():
    for _cmd in (cmd, ghi.commands.release.cmd):
        _cmd.callback(invoke_without_command=True)(default_invoke_without_command)


if __name__ == "__main__":
    add_default_invoke()
    cmd()
