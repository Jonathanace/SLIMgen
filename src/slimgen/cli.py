from typing import Optional

import typer

from .groupchat import cli


app = typer.Typer()

@app.command() # old usage: from .groupchat import cli; app.command()(cli)
def main(
    usage: str = typer.Argument(None),
):
    print(f'Starting main, {usage}')

if __name__ == "__main__":
    app()