import os
import sys
from dataclasses import dataclass
from typing import Optional

import typer

from clip import __version__
from clip.clipboard import Clipboard

DEFAULT_CLIP_CACHE_FILE = f"{os.environ['HOME']}/.clip.json"
CLIP_CACHE_ENV_VAR = "CLIP_CACHE_FILE"

app = typer.Typer(name="clip", add_completion=False)


@dataclass
class ClipContext:
    cache_file_path: str


def version_callback(value: bool):
    if value:
        print(f"Clip Version: {__version__}")
        raise typer.Exit()


def set_cache_file_callback(ctx: typer.Context, path: str):
    ctx.obj = ClipContext(path)


def show_callback(ctx: typer.Context, value: bool):
    if value:
        with Clipboard(ctx.obj.cache_file_path) as clip:
            clip.show_registers()
        raise typer.Exit()


def reset_callback(ctx: typer.Context, value: bool):
    if value:
        with Clipboard(ctx.obj.cache_file_path) as clip:
            clip.reset_registers()
        raise typer.Exit()


@app.command(
    help="A command line utility for managing multiple clipboards.",
)
def main(
    ctx: typer.Context,
    register: str = typer.Argument(
        ..., help="The register to copy to/paste from.", show_default=False
    ),
    content: Optional[str] = typer.Argument(
        None if sys.stdin.isatty() else sys.stdin.read().strip(),
        help="The content to copy (can be redirected from stdin). If no content is specified, clip performs a paste.",
    ),
    clear: bool = typer.Option(
        False, "--clear", "-c", help="Clears the specified register."
    ),
    version: Optional[bool] = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Print version information.",
    ),
    cache_file: Optional[str] = typer.Option(
        DEFAULT_CLIP_CACHE_FILE,
        "--cache-file",
        "-f",
        help="Specify the path to the file where the register contents will be stored.",
        envvar=CLIP_CACHE_ENV_VAR,
        is_eager=True,
        callback=set_cache_file_callback,
    ),
    show: Optional[bool] = typer.Option(
        False,
        "--list",
        "-l",
        help="Show the contents of all registers as a json string.",
        callback=show_callback,
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        "-r",
        help="Clears all registers.",
        callback=reset_callback,
    ),
):
    with Clipboard(ctx.obj.cache_file_path) as clip:
        if content is None and not clear:
            typer.echo(clip[register])
        elif not clear:
            clip[register] = content

        if clear:
            del clip[register]
