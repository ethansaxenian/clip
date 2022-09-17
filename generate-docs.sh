# A script to generate docs using typer-cli

# typer-cli is currently incompatible with the latest versions of typer and black
# so remove them and temporarily install typer-cli (and its outdated dependencies)
poetry remove typer black
poetry add typer-cli

typer clip/main.py utils docs --name clip --output DOCS.md

# finally, uninstall typer-cli and reinstall typer and black with latest versions
poetry remove typer-cli
poetry add typer
poetry add black -G dev
poetry lock
