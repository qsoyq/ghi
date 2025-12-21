import typer
from ghi.utils import version_callback, error, is_cmd_exists


def default_invoke_without_command(
    _: bool = typer.Option(False, "--version", "-v", "-V", callback=version_callback),
):
    if not is_cmd_exists("gh"):
        typer.echo(error("gh not found"))
        raise typer.Exit(-1)
