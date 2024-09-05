import typer
from typing_extensions import Annotated

def main(arg1: Annotated[str, typer.Argument(help="idk")] = ""):
    print('Slimgen executed!')