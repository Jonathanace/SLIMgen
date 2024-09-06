import typer

from .main import main
from .groupchat import groupchat_yzhu_cust


app = typer.Typer()
app.command()(groupchat_yzhu_cust)


if __name__ == "__main__":
    app()