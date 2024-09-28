import typer
from typing_extensions import Annotated

def main(arg1: Annotated[str, typer.Argument(help="Main arg")] = ""):
    if arg1 == "webui":
        print('webui')
    print('Slimgen executed!')