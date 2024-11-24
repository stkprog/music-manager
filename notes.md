# keeping track of things

## curses
### terminal resizing
* minimal example:
    - when resizing the terminal window with the mouse, the key from ``getkey()`` is called **KEY_RESIZE**
    - this also works with XFCE4's resizing shortcut (_Alt+F8_)
    - ``curses.update_lines_cols()`` updates the numbers
    - current values can be accessed using ``stdscr.getmaxyx()``
    - program doesn't terminate when resizing (!!!)
```
def main(stdscr : window):
    while(True):
        y, x = stdscr.getmaxyx()
        update_lines_cols()

        stdscr.clear()
        stdscr.addstr(0, 1, "height: " + str(y), A_NORMAL)
        stdscr.addstr(1, 1, "width: " + str(x), A_NORMAL)
        stdscr.addstr(2, 1, key)
        stdscr.refresh()
        key = stdscr.getkey()
wrapper(main)
```
### header lines
* minimal examples:
```
def initialize_header_edge_aligned(stdscr : window, side : str, y : int):
    max_term_width : int = stdscr.getmaxyx()[1]
    header_text : str = "Music-Manager 0.1"
    remaining_space : int = max_term_width - len(header_text)

    if side == "left":
        header_text += " " * remaining_space
    elif side == "right":
        header_text = " " * remaining_space + header_text

    stdscr.addstr(y, 0, header_text)
```
* for this one, the center position is calculated by:
    - dividing the maximum width by 2
    - subtracting half of the width of the text that is to be positioned in the center
```
def initialize_header_center(stdscr : window, y):
    max_term_width : int = stdscr.getmaxyx()[1]
    header_text : str = "Music-Manager 0.1"
    
    space_before : int = int((max_term_width / 2) - (len(header_text) / 2))
    space_after : int = max_term_width - (space_before + len(header_text))
    header_text = (" " * space_before) + header_text + (" " * space_after)

    stdscr.addstr(y, 0, header_text)
```

### footer line
* minimal example:
```
def initialize_footer(stdscr : window, color : int):
    max_term_height : int = stdscr.getmaxyx()[0] - 1
    max_term_width : int = stdscr.getmaxyx()[1]

    text : tuple = ("G", "Quit", "S", "Save")

    stdscr.move(max_term_height, 0) # Move cursor down to final line
    for i in range(len(text)):
        # Single Character ("Q", "S")
        if i % 2 == 0:
            stdscr.addstr(text[i], color | A_REVERSE)
        # Action word ("Quit", "Save")
        elif i % 2 == 1:
            stdscr.addstr(" " + text[i] + "   ", color)

    current_position : int = stdscr.getyx()[1]
    remaining_space : int = max_term_width - current_position - 1
    stdscr.addstr(" " * remaining_space, color)
    # Fill bottom right corner with given attribute
    # If a string of length 1 or char isn't passed, a caret (^) will be shown
    stdscr.insch(" ", color)
```

### pads
* fixed window that is seen, content inside "moves"
* test strings always seemed to be cut off by atleast one character on the left side

## local file management
* save both of the following on any change, for safety?
### bucketlist albums
* no additional information from user here
* so could save as an array of IDs (from discogs) in a .json array
* load in program as array?
```
[
    3612706,
    3643167,
    3252004
]
```
### listened to albums
* user should be able to give ratings and perhaps their thoughts on an album
* saved in .json as an array of objects?
* load in program as an array of class-objects?
```
[
    {
        "release_id": 3612706,
        "rating": 6,
        "thoughts": "lorem ipsum"
    },
    {
        "release_id": 3643167,
        "rating": 3,
        "thoughts": "ipsum lorem"
    },
    {
        "release_id": 3252004,
        "rating": 6,
        "thoughts": "lorem ipsum"
    }
]
```
* either that, or take info from discogs and save it all locally:
```
[
    {
        "artist": "lorem",
        "album": "ipsum",
        "year": 2000,
        "genre": "dolor",
        "rating": 6,
        "thoughts": "lorem ispum dolor..." 
    },
    // ...
]
```
* not sure yet which option would be the better one
* realistically probably the first one. i'm using the discogs api for a reason
* should probably check if the api has access limits
* if not, experiment with caching

## asciimatics
* considering changing to this libary, because it's higher level than curses

### themes
* default theme dictionary can be imported using
```
from asciimatics.widgets.utilities import THEMES
```
* i'm not sure if this is the case for every tty, but on mine, "BOLD" text is shown lighter as "NORMAL" text
### example scene structure
* scene
    - frame
        * layout
        * layout
    - frame
        * layout
* <u>LAYOUTS:</u>
    - hold widgets in a specified amount of columns
    - columns can be the same width (1, 1) or different widths (2, 1)
* <u>FRAMES:</u>
    - hold layouts
    - can be scrollable or not
* <u>SCENES:</u>
    - hold frames
    - can be switched to using the ``NextScene`` exception and an identifier

### event handling
* this includes keyboard presses and mouse clicks
* only certain things are already handled by widgets
* everything else is unhandled
* for such events, define a function at the top as such
```
def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        c = chr(event.key_code)
        if c == "q" or c == "Q":
            raise StopApplication("User terminated app")
```
* and then make sure this function is called for unhandled inputs
```
screen.play(..., unhandled_input=global_shortcuts, ...)
```
* function keys etc. can be accessed using ``Screen.KEY_F1``. These are all integer numbers

### tabular data
* the widget ``MultiColumnListBox`` exists for this purpose
* the column names are initialized as a simple list of strings
* the data rows are initialized as a list of tuples that contain a list (data) and an integer (ALBUM RELEASE ID!) see the following:
```
data = [
    (["2024", "Machine Girl", "MG Ultra", "Electronic", "10"], 0),
    (["2018", "Machine Girl", "The Ugly Art", "Electronic", "9"], 1)
]
```
* the ``MultiColumnListBox`` supports the up and down arrow keys for selecting an entry. the current entry's internal value (ALBUM RELEASE ID IN MY CASE) can be gotten from ``self.name_of_list_widget.value``
* the column widths can be initialized as such:
    - ``">6"`` == a right aligned column that is 6 characters wide
    - ``"<20%"`` == a left aligned column with a width of 20% of the widget
    - ``"^0"`` == a center aligned column that takes up the rest of the space available

### popups
* i'm going to need several popup frames for this program:
    - one for editing the rating
    - one for viewing / editing the thoughts
    - one for searching and adding new albums to the bucket list
    - one for searching and adding new albums to the listened list + ability to add rating & thoughts
* asciimatics does offer a class called ``PopUpDialog`` which is a good starting point for this purpose, but it isn't exactly suited to my needs. because the code for that class isn't very long, i'm going to write my own implementation(s) for these use cases

## ui / album management
* the differents sections should act as different screens that get "switched out", similar to the notebook widget in gtk. think tabs
* tab name includes the corresponding buttons to load the tab, ideally something simple like f1 ... f10
* bottom of the screen shows q for quit, etc
* a window with a textbox should pop up when the user types something, below the results from the search
* ability to delete items from the bucketlist OR move them to the "listened" list
* ability to change rating and thoughts for listened to albums
* ability to sort albums in both lists by the different columns

## discogs API
* some artists share the same names, so they are made identifiable by adding the number at the end e.g. (2)
* to remove this using string cutting: ``artist_name[:-4]``

## things to note / useful links
* initializing locales so characters of all languages(?) work: [here](https://stackoverflow.com/questions/42510606/python-curses-textpad-textbox-keyboard-input-not-working-with-german-umlauts)
* [textbox selection example](https://incolumitas.com/2013/06/02/python-and-curses-a-small-textbox-selection-example/)
* [scrolling menu example](https://stackoverflow.com/questions/30828804/how-to-make-a-scrolling-menu-in-python-curses)
* [Curses Programming with Python by A.M. Kuchling](https://sceweb.sce.uhcl.edu/helm/WEBPAGE-Python/documentation/howto/curses/curses.html)
* [Ncurses: Pads](https://de.wikibooks.org/wiki/Ncurses:_Pads)
* [python-curses-scroll-example](https://github.com/mingrammer/python-curses-scroll-example/tree/master)
* [python_curses_examples](https://github.com/itssme/python_curses_examples)