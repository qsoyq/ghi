import typer
from typer_utils.utils import error, is_cmd_exists, version_callback


def default_invoke_without_command(
    _: bool = typer.Option(False, "--version", "-v", "-V", callback=lambda echo: version_callback(echo, module_name="ghi")),
):
    if not is_cmd_exists("gh"):
        typer.echo(error("gh not found"))
        raise typer.Exit(-1)
