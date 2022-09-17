# Clip

A simple command-line utility that provides vim-like copy/paste with registers.

Currently, `clip` does ***not*** interact with the system copy and paste functionality (e.g. <kbd>⌘</kbd>+<kbd>c</kbd>/<kbd>⌘</kbd>+<kbd>v</kbd> on macos).

## Usage

See [docs](./DOCS.md) or run `clip --help`.

## Configuration

`clip` respects the environment variable `CLIP_CACHE`, which defaults to `$HOME/.clip.json`. This defines the file where the register contents will be stored.
