import json
import os

import pytest
from typer.testing import CliRunner

from clip import __version__
from clip.clipboard import Clipboard
from clip.main import app

TEST_CACHE_FILE = "test_cache_file"

TEST_CLIPBOARD = {"1": "foo", "2": "bar", "3": "baz"}

runner = CliRunner(env={"CLIP_CACHE_FILE": TEST_CACHE_FILE})


def load_test_clipboard():
    with Clipboard(TEST_CACHE_FILE) as clip:
        clip.registers = TEST_CLIPBOARD


def get_test_file_contents() -> dict[str, str]:
    with open(TEST_CACHE_FILE, "r") as file:
        return json.load(file)


@pytest.fixture(autouse=True)
def after_each():
    yield
    with Clipboard(TEST_CACHE_FILE) as clip:
        clip.registers = {}


def test_version():
    result = runner.invoke(app, ["--version"])
    assert __version__ in result.stdout


def test_list():
    load_test_clipboard()
    result = runner.invoke(app, ["--list"])
    for k, v in TEST_CLIPBOARD.items():
        assert f'"{k}": "{v}"' in result.stdout


def test_list_empty():
    result = runner.invoke(app, ["--list"])
    assert "Clipboard is empty." in result.stdout


def test_reset():
    load_test_clipboard()
    result = runner.invoke(app, ["--reset"])
    assert "Clearing registers..." in result.stdout
    clip = get_test_file_contents()
    assert len(clip.items()) == 0


def test_copy():
    runner.invoke(app, ["1", "foo"])
    clip = get_test_file_contents()
    assert clip["1"] == "foo"


def test_copy_replaces_existing():
    load_test_clipboard()
    runner.invoke(app, ["1", "replaced"])
    clip = get_test_file_contents()
    assert clip["1"] == "replaced"


def test_paste():
    load_test_clipboard()
    result = runner.invoke(app, ["1"])
    assert "foo" in result.stdout


def test_paste_bad_register():
    load_test_clipboard()
    result = runner.invoke(app, ["not-a-register"])
    assert f"Buffer 'not-a-register' not found." in result.stdout


def test_clear():
    load_test_clipboard()
    runner.invoke(app, ["-c", "1"])
    clip = get_test_file_contents()
    assert clip.get("1") is None


def test_creates_file_if_not_exists():
    os.remove(TEST_CACHE_FILE)
    runner.invoke(app, ["1", "foo"])
    clip = get_test_file_contents()
    assert clip["1"] == "foo"
