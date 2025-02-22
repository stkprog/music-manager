from frontendcli.tui import enter

import os
import sys
import click

from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

@click.command
def start() -> None:
    last_scene = None
    # Program Loops
    while True:
        # Start the Scene. last_scene is passed to enter()
        try:
            Screen.wrapper(
                func=enter, catch_interrupt=False, arguments=[last_scene]
            )
            sys.exit(os.EX_OK)
        # Handle the Screen being resized
        except ResizeScreenError as error:
            last_scene = error.scene

start()