from frontendcli.loop import enter

import sys

from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

last_scene = None
# Program Loops
while True:
    # Start the Scene. last_scene is passed to enter()
    try:
        Screen.wrapper(
            func=enter, catch_interrupt=False, arguments=[last_scene]
        )
        sys.exit(0)
    # Handle the Screen being resized
    except ResizeScreenError as error:
        last_scene = error.scene