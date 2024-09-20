import typer

from .groupchat import cli


app = typer.Typer()
app.command()(cli)


if __name__ == "__main__":
    app()