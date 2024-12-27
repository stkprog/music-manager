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
    - 1: searching and adding new albums to the bucketlist USING DISCOGS
        * only callable from the BUCKET tab
        * a small textbox for entering a search term
        * output and selection using a multicolumnbox
        * adding on enter-press?
        * "cancel" as a button
    - 2: adding new albums to the bucketlist MANUALLY
        * only callable from the BUCKET tab
        * a small form for entering all the values
        * a requirement for this is some kind of functionality that keeps track of release_id's for manually added tracks - perhaps just counting up from 1
        * "add" and "cancel" as buttons
    - 3: adding new albums to the listened list
        * only callable from the BUCKET tab
        * a small form showing the data of the album and allowing the user to enter rating and thoughts
        * "add to listened" and "cancel" as buttons 
    - 4: editing the rating and thoughts
        * only callable from the LISTENED tab
        * rating and thoughts as textboxes?
        * "change" and "cancel" as buttons
* asciimatics does offer a class called ``PopUpDialog`` which is a good starting point for this purpose, but it isn't exactly suited to my needs. because the code for that class isn't very long, i'm going to write my own implementation(s) for these use cases
* 3 and 4 would probably look identical, so i wonder if there would be a way to combine them
* loading data into widgets:
    - using the dedicated ``data`` variable from the class ``Frame`` or the ``value`` variable from the specific widget ([src](https://asciimatics.readthedocs.io/en/stable/widgets.html#setting-values))
    * i might use the former method for the ``MultiColumnListBox``es containing the user's saved albums, and the latter method for PopUps

listened_tab_data = {

}
---
* some possible pseudo-code:
```
*-*-*-*-*-*-*-*-*-* 2: adding new albums to the bucketlist MANUALLY *-*-*-*-*-*-*-*-*-*

SomePopUp:
...
# PopUp title = "Add a bucket album manually"
layout1 = Layout([1])
self.add_layout(layout1)

# Artist(s)
layout1.add_widget(Text(
    label="Artist(s):",
    name="",
    on_chance="",
    validator="some_optional_regex"
))

# Title
layout1.add_widget(Text(
    label="Title:",
    name="",
    on_chance="",
    validator="some_optional_regex"
))

# Year
layout1.add_widget(Text(
    label="Year:",
    name="",
    on_chance="",
    validator="some_optional_regex"
))

# Genre(s)
layout1.add_widget(Text(
    label="Genre(s):",
    name="",
    on_chance="",
    validator="some_optional_regex"
))



*-*-*-*-*-*-*-*-*-* 4: editing the rating and thoughts *-*-*-*-*-*-*-*-*-*

SomePopUp:
...
# PopUp title = "Edit rating and thoughts"
layout1 = Layout([1])
self.add_layout(layout1)
layout1.add_widget(
    Label("title by artist (year) [genre]"), 1
)

layout2 = Layout([1, 15])
self.add_layout(layout2)
layout2.add_widget(
    Label("Rating:"), 1
)
# Put in existing value
layout2.add_widget(
    DropdownList(
        options=tuple([str(i + 1), i + 1] for i in range(10)),
        label="Rating",
        name="",
        on_chance="",
        ...
    ),
    2
)

layout2.add_widget(
    TextBox(
        height=10,
        label="Thoughts",
        name="",
        parser=AsciimaticsParser(),
        line_wrap=True,
        on_change=""
    ), 2
)
```

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
* archived code:
```
def search_multiple(self, user_query : str) -> list[BucketAlbum]:
    """Search for the main release of albums using the text provided by the user."""
    results : MixedPaginatedList = self.d.search(user_query, type="master").page(1)[0:10]
    artists : str = ""
    processed_results : list[BucketAlbum] = []

    # Searching for "master releases" instead of "releases"
    # and then the main release. multiple releases of the same album
    # e.g. in different formats (LP, CD, ...) don't need to be shown to the user.
    for r in results:                       # r = Master
        main_r : Release = r.main_release   # main_r = Release
        artists = []
        for a in main_r.artists:
            artists.append(self.process_artist(a.name))
        artists = self.array_to_comma_separated_string(artists)
        genres = self.array_to_comma_separated_string(main_r.genres)
        year : int | str = self.process_year(r, main_r)

        processed_results.append(BucketAlbum(
            main_r.id, artists, main_r.title, genres, year
        ))
    return processed_results
```

## things to note / useful links
* initializing locales so characters of all languages(?) work: [here](https://stackoverflow.com/questions/42510606/python-curses-textpad-textbox-keyboard-input-not-working-with-german-umlauts)
* [textbox selection example](https://incolumitas.com/2013/06/02/python-and-curses-a-small-textbox-selection-example/)
* [scrolling menu example](https://stackoverflow.com/questions/30828804/how-to-make-a-scrolling-menu-in-python-curses)
* [Curses Programming with Python by A.M. Kuchling](https://sceweb.sce.uhcl.edu/helm/WEBPAGE-Python/documentation/howto/curses/curses.html)
* [Ncurses: Pads](https://de.wikibooks.org/wiki/Ncurses:_Pads)
* [python-curses-scroll-example](https://github.com/mingrammer/python-curses-scroll-example/tree/master)
* [python_curses_examples](https://github.com/itssme/python_curses_examples)