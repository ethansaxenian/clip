# `clip`

A command line utility for managing multiple clipboards.

**Usage**:

```console
$ clip [OPTIONS] REGISTER [CONTENT]
```

**Arguments**:

* `REGISTER`: The register to copy to/paste from.  [required]
* `[CONTENT]`: The content to copy (can be redirected from stdin). If no content is specified, clip performs a paste.

**Options**:

* `-c, --clear`: Clears the specified register.  [default: False]
* `-V, --version`: Print version information.  [default: False]
* `-f, --cache-file TEXT`: Specify the path to the file where the register contents will be stored.  [env var: CLIP_CACHE_FILE; default: /Users/ethansaxenian/.clip.json]
* `-l, --list`: Show the contents of all registers as a json string.  [default: False]
* `-r, --reset`: Clears all registers.  [default: False]
* `--help`: Show this message and exit.
