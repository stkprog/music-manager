# keeping track of things

## local file management
* save both of the following on any change, for safety?
### bucketlist albums
```
[
    {
        "release_id": 34234,
        "artists": "lorem",
        "title": "ipsum",
        "genres": "hip hop",
        "year": 2003
    }
]
```
### listened to albums
* user should be able to give ratings and perhaps their thoughts on an album
```
[
    {
        "release_id": 25345436,
        "artists": "lorem",
        "title": "ipsum",
        "genres": "dolor",
        "year": 2000,
        "rating": 6,
        "thoughts": "lorem ispum dolor..." 
    }
]
```
* this is very much redundant, but because the discogs api is limited to one query per second, this is going to be the simpler solution for now

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
            - widget
            - widget
        * layout
            - widget
    - frame
        * layout
            - widget
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
* <u>i'm going to need several popup frames for this program:</u>
    - editing the rating and thoughts
        * only callable from the LISTENED tab
        * rating and thoughts as textboxes?
        * "change" and "cancel" as buttons
    - searching and adding new albums to the bucketlist USING DISCOGS
        * only callable from the BUCKET tab
        * a small textbox for entering a search term
        * output and selection using a multicolumnbox
        * adding on enter-press?
        * "cancel" as a button
    - adding new albums to the bucketlist MANUALLY
        * only callable from the BUCKET tab
        * a small form for entering all the values
        * a requirement for this is some kind of functionality that keeps track of release_id's for manually added tracks - perhaps just counting up from 1
        * "add" and "cancel" as buttons
    - adding new albums to the listened list
        * only callable from the BUCKET tab
        * a small form showing the data of the album and allowing the user to enter rating and thoughts
        * "add to listened" and "cancel" as buttons 
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