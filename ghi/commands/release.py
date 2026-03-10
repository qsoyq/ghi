import shlex
import subprocess
from typing import Optional

import typer
from typer_utils.utils import get_project_version

cmd = typer.Typer(help="A wrapper for github cli release command.")


def run_command(command: str, verbose: bool = False) -> subprocess.CompletedProcess[str]:
    if verbose:
        typer.echo(f"cmd: {command}")
    return subprocess.run(shlex.split(command), capture_output=True, text=True)


def delete_tag_refs(tag: str, verbose: bool = False) -> None:
    # Best effort: remove both local and remote tags so recreate can retarget.
    local_delete = run_command(f"git tag -d {tag}", verbose=verbose)
    if local_delete.returncode != 0 and "not found" not in local_delete.stderr.lower():
        typer.echo(local_delete.stderr, err=True, color=True)
        raise typer.Exit(local_delete.returncode)

    remote_delete = run_command(f"git push origin :refs/tags/{tag}", verbose=verbose)
    if remote_delete.returncode != 0 and "remote ref does not exist" not in remote_delete.stderr.lower():
        typer.echo(remote_delete.stderr, err=True, color=True)
        raise typer.Exit(remote_delete.returncode)


@cmd.callback(invoke_without_command=True)
def default(): ...


@cmd.command()
def create(
    tag: str | None = typer.Option(None, "--tag", help="Release tag,  use the version from pyproject.toml as the default release tag"),
    title: str = typer.Option("", "-t", "--title", help="Release title"),
    target: str = typer.Option("", "--target", help="Target branch or full commit SHA (default: main branch)"),
    notes: str = typer.Option("", "--notes", "-n", help="Release notes"),
    prerelease: bool | None = typer.Option(None, "-p", "--prerelease ", help="Mark the release as a prerelease"),
    recreate: bool = typer.Option(False, "--recreate", help="Delete the release if it already exists before creating"),
    verbose: bool = typer.Option(False, "--verbose"),
):
    """Create a new gitHub release for a repository."""
    # TODO: add release assets
    if tag is None:
        version = get_project_version()
        tag = version

    if recreate:
        check_cmd = f"gh release view {tag}"
        check_result = run_command(check_cmd, verbose=verbose)
        if check_result.returncode == 0:
            if verbose:
                typer.echo(f"Release {tag} exists, deleting it first...")
            delete_cmd = f"gh release delete -y {tag}"
            delete_result = run_command(delete_cmd, verbose=verbose)
            if delete_result.returncode != 0:
                typer.echo(delete_result.stderr, err=True, color=True)
                raise typer.Exit(delete_result.returncode)
            delete_tag_refs(tag, verbose=verbose)

    cmd = "gh release create"
    if notes:
        cmd += f" --notes {notes}"
    else:
        cmd += " --generate-notes"

    if prerelease:
        cmd += " --prerelease"

    if target:
        cmd += f" --target {target}"

    if title:
        cmd += f" -t {title}"

    cmd += f" {tag}"
    args = shlex.split(cmd)
    if verbose:
        typer.echo(f"cmd: {cmd}")

    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        typer.echo(p.stderr, err=True, color=True)
        raise typer.Exit(p.returncode)

    typer.echo(p.stdout)


@cmd.command()
def delete(
    tag: Optional[str] = typer.Option(None, "--tag"),
    verbose: Optional[bool] = typer.Option(
        None,
        "--verbose",
    ),
    skip_prompt: bool = typer.Option(True, "-y", "--yes", help="Skip the confirmation prompt"),
    delete_tag: bool = typer.Option(True, "--delete-tag"),
):
    """Delete a release."""
    cmd = "gh release delete"
    if tag is None:
        version = get_project_version()
        tag = version

    if skip_prompt:
        cmd += " -y"

    cmd += f" {tag}"
    args = shlex.split(cmd)
    if verbose:
        typer.echo(f"cmd: {cmd}")

    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        typer.echo(p.stderr, err=True, color=True)
        raise typer.Exit(p.returncode)

    typer.echo(p.stdout)
    if not delete_tag:
        return

    delete_tag_refs(tag, verbose=bool(verbose))


if __name__ == "__main__":
    cmd()
