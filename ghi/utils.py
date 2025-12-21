import subprocess
from pathlib import Path
from functools import cache
import typer
import toml


@cache
def get_pyproject_data() -> dict:
    "从当前路径递归向上查找 pyproject.toml"
    p = Path("./pyproject.toml")
    while not p.exists():
        if not p.parent:
            raise RuntimeError("pyproject.toml not exists.")
        p = p.parent / "pyproject.toml"

    if not p.is_file():
        raise TypeError("pyproject.toml must be file.")

    data = toml.load(p)
    return data


def get_project_name() -> str | None:
    data = get_pyproject_data()
    return data.get("project", {}).get("name")


def get_project_version() -> str | None:
    data = get_pyproject_data()
    return data.get("project", {}).get("version")


def version_callback(value: bool):
    if value:
        name = get_project_name()
        version = get_project_version()
        typer.echo(f"{name} cli version: {version}")
        raise typer.Exit()


def is_cmd_exists(executable: str) -> bool:
    p = subprocess.run(f"command -v {executable}", shell=True, capture_output=True)
    return p.returncode == 0


def error(message: str) -> str:
    return typer.style(message, fg=typer.colors.WHITE, bg=typer.colors.RED)
