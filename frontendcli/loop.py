from backend.discogs import DiscogsHelper
from backend.files import FileWriter
from backend.models import Listened
from backend.models import ProcessedRelease
from curses import *
from curses import textpad

def get_token() -> str:
    """Reads and returns the Discogs API personal access token from the specified file."""
    return open("token.txt", "r").read()

def initialize_curses_colors() -> None:
    init_pair(1, COLOR_BLACK, COLOR_WHITE)
    init_pair(2, COLOR_BLACK, COLOR_BLACK)
    init_pair(3, COLOR_WHITE, COLOR_WHITE)
    init_pair(4, COLOR_WHITE, COLOR_RED)
    init_pair(5, COLOR_WHITE, COLOR_BLUE)

def enter(stdscr : window) -> None:
    """Entrypoint for the main loop of the program."""
    file_writer = FileWriter()
    discogs_helper = DiscogsHelper(get_token())

    initialize_curses_colors()
    DEFAULT = color_pair(1)
    BLACK = color_pair(2)
    WHITE = color_pair(3)
    RED = color_pair(4)
    BLUE = color_pair(5)
    curs_set(0)

    y, x = stdscr.getmaxyx()
    stdscr.bkgd(" ", BLACK)

    header_win : window = newwin(1, x, 0, 0)
    header_win.bkgd(" ", WHITE)

    content_win : window = newwin(y - 1, x, 1, 0)
    content_win.bkgd(" ", RED)

    input_win : window = newwin(1, 20, 1, 0)
    input_win.bkgd("_", DEFAULT)
    input_box = textpad.Textbox(input_win)

    key = ""
    user_input = ""
    while True:
        # stdscr.addstr(0, 0, "str")
        if key == "q" or key == "Q":
            break
        elif key == "1":
            content_win.bkgd(" ", BLUE)
        elif key == "2":
            content_win.bkgd(" ", RED)
        elif key == "t" or key == "T":
            input_box.edit()
            user_input = input_box.gather().strip()
        
        # header_win.bkgd(" ", WHITE)
        stdscr.refresh()
        header_win.refresh()
        content_win.clear()
        content_win.addstr(1, 0, user_input)
        content_win.refresh()
        # input_win.clear()
        input_win.refresh()
        key = stdscr.getkey()

    ### TESTING
    # master_release = discogs_helper.get_release(3643167)
    
    # test : list[ProcessedRelease] = discogs_helper.search(input())
    # for x in test:
    #     print(x)

    # file_writer.ensure_files_exist()
    # file_writer.read_album_list()
    # file_writer.remove_from_album_list(123)
    # file_writer.remove_from_album_list(235346546)