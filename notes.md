# keeping track of things

## curses
### terminal resizing
* minimal example:
    - when resizing the terminal window with the mouse, the key from ``getkey()`` is called **KEY_RESIZE**
    - this also works with XFCE4's resizing shortcut (_Alt+F8_)
    - ``curses.update_lines_cols()`` updates the numbers
    - current values can be accessed using ``stdscr.getmaxyx()``
```
def main(stdscr : window):
    while(True):
        y, x = stdscr.getmaxyx()
        key = stdscr.getkey()

        update_lines_cols()

        stdscr.clear()
        stdscr.addstr(0, 1, "height: " + str(y), A_NORMAL)
        stdscr.addstr(1, 1, "width: " + str(x), A_NORMAL)
        stdscr.addstr(2, 1, key)
        stdscr.refresh()
wrapper(main)
```

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

## ui / album management
* the differents sections should act as different screens that get "switched out", similar to the notebook widget in gtk. think tabs
* tab name includes the corresponding buttons to load the tab, ideally something simple like f1 ... f10
* bottom of the screen shows q for quit, etc
* a window with a textbox should pop up when the user types something, below the results from the search
* ability to delete items from the bucketlist OR move them to the "listened" list
* ability to change rating and thoughts for listened to albums
* ability to sort albums in both lists by the different columns

## things to note / useful links
* initializing locales so characters of all languages(?) work: [here](https://stackoverflow.com/questions/42510606/python-curses-textpad-textbox-keyboard-input-not-working-with-german-umlauts)
* [textbox selection example](https://incolumitas.com/2013/06/02/python-and-curses-a-small-textbox-selection-example/)
* [scrolling menu example](https://stackoverflow.com/questions/30828804/how-to-make-a-scrolling-menu-in-python-curses)