import json
import os
import sys
from typing import Optional

import typer

__version__ = "0.1.0"

default_cache_file = f"{os.environ['HOME']}/.clip.json"
cache_file = os.environ.get("CLIP_CACHE_FILE", default_cache_file) or default_cache_file


class Clipboard:
    registers: dict[str, str]

    def load_registers(self):
        try:
            with open(cache_file, "r") as buf_file:
                self.registers = json.load(buf_file)
        except FileNotFoundError:
            self.registers = {}

    def save_registers(self):
        with open(cache_file, "w+") as buf_file:
            json.dump(self.registers, buf_file, ensure_ascii=False)

    def __enter__(self) -> dict[str, str]:
        self.load_registers()
        return self.registers

    def __exit__(self, exc_type, exc_value, exc_tb) -> bool:
        if exc_type is KeyError:
            print(f"Buffer {exc_value} not found.", file=sys.stderr)
            return True

        self.save_registers()


app = typer.Typer(
    name="clip",
    add_completion=False,
)


def version_callback(value: bool):
    if value:
        print(f"Clip Version: {__version__}")
        raise typer.Exit()


def show_callback(value: bool):
    if value:
        with Clipboard() as clip:
            if clip:
                print(json.dumps(clip, ensure_ascii=False, indent=2, sort_keys=True))
            else:
                print("Clipboard is empty.")
        raise typer.Exit()


def reset_callback(value: bool):
    if value:
        with Clipboard() as clip:
            print("Clearing clipboard...")
            clip.clear()
        raise typer.Exit()


@app.command(
    help="A command line utility for managing multiple clipboards.",
)
def main(
    register: str = typer.Argument(..., help="The register to copy to/paste from."),
    content: Optional[str] = typer.Argument(
        None if sys.stdin.isatty() else sys.stdin.read().strip(),
        help="The content to copy (can be redirected from stdin). If no content is specified, clip performs a paste.",
    ),
    clear: bool = typer.Option(
        False, "--clear", "-c", help="Clears the specified register."
    ),
    show: Optional[bool] = typer.Option(
        False,
        "--show",
        "-s",
        help="Show the contents of all registers as a json string.",
        is_eager=True,
        callback=show_callback,
    ),
    version: Optional[bool] = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Print version information.",
    ),
    reset: bool = typer.Option(
        False,
        "--reset",
        "-r",
        help="Clears all registers.",
        callback=reset_callback,
        is_eager=True,
    ),
):
    with Clipboard() as clip:
        if content is None and not clear:
            print(clip[register])
        elif not clear:
            clip[register] = content

        if clear:
            del clip[register]
