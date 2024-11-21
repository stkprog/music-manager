from frontendcli import loop
from curses import wrapper

wrapper(loop.enter)