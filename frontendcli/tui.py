from backend.discogs import DiscogsHelper
from backend.files import FileWriter
from backend.models import BucketAlbum, ListenedAlbum

import sys
import string
import random

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, MultiColumnListBox, Widget, Label, PopUpDialog, TextBox, Text, Divider
from asciimatics.widgets.utilities import THEMES
from asciimatics.event import Event, KeyboardEvent, MouseEvent
from asciimatics.exceptions import NextScene, ResizeScreenError, StopApplication

THEMES["music-manager"] = {
    #                   FOREGROUND                          ATTRIBUTE           BACKGROUND
    "background": (Screen.COLOUR_WHITE,                 Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK,                     None,               Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_BLACK,                   Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_YELLOW,                   Screen.A_BOLD,      Screen.COLOUR_RED),
    "label": (Screen.COLOUR_BLUE,                       Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "borders": (Screen.COLOUR_WHITE,                    Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_WHITE,                     Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "title": (Screen.COLOUR_CYAN,                       Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "edit_text": (Screen.COLOUR_BLACK,                  Screen.A_BOLD,      Screen.COLOUR_WHITE),
    "focus_edit_text": (Screen.COLOUR_BLACK,            Screen.A_NORMAL,    Screen.COLOUR_WHITE),
    "readonly": (Screen.COLOUR_BLUE,                    Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "focus_readonly": (Screen.COLOUR_YELLOW,            Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "button": (Screen.COLOUR_WHITE,                     Screen.A_NORMAL,    Screen.COLOUR_BLUE),
    "focus_button": (Screen.COLOUR_WHITE,               Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "control": (Screen.COLOUR_CYAN,                     Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_control": (Screen.COLOUR_GREEN,           Screen.A_BOLD,      Screen.COLOUR_BLUE),
    "focus_control": (Screen.COLOUR_CYAN,               Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_focus_control": (Screen.COLOUR_CYAN,      Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "field": (Screen.COLOUR_WHITE,                      Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_WHITE,             Screen.A_NORMAL,    Screen.COLOUR_BLUE),
    "focus_field": (Screen.COLOUR_WHITE,                Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_WHITE,       Screen.A_BOLD,      Screen.COLOUR_BLUE),
}

test_data = [
    (["2024", "Machine Girl", "MG Ultra", "Electronic", "10"], 1243465),
    (["2018", "Machine Girl", "The Ugly Art", "Electronic", "9"], 1),
    (["2002", "Boards of Canada", "Music Has the Right to Children", "Genre", "10"], 2),
    (["2017", "Machine Girl", "...Because I'm Young Arrogant and Hate Everything You Stand For", "Genre", "10"], 3),
    (["2015", "Machine Girl", "Gemini", "Genre", "10"], 4),
    (["2018", "Machine Girl", "The Ugly Art", "Genre", "10"], 5),
    (["2020", "Machine Girl", "U-Void Synthesizer", "Genre", "10"], 6),
    (["2023", "Black Midi", "Hellfire", "Genre", "10"], 7),
    (["2022", "Black Midi", "Cavalcade", "Genre", "10"], 8),
    (["2021", "Black Midi", "Schlagenheim", "Genre", "10"], 9),
    (["2002", "Madvillain", "Madvillainy", "Genre", "10"], 10),
    (["2002", "Boards of Canada", "Geogaddi", "Genre", "10"], 11),
    (["2003", "Aphex Twin", "Druqks", "Genre", "10"], 12),
    (["1999", "Aphex Twin", "Selected Ambient Works", "Genre", "10"], 13),
    (["1970", "Radiohead", "In Rainbows", "Genre", "10"], 14),
    (["1996", "Radiohead", "OK Computer", "Genre", "10"], 15),
    (["????", "King Crimson", "Red", "Genre", "10"], 16),
    (["1981", "King Crimson", "In the Hall of the Crimson King", "Genre", "10"], 17),
    (["2000", "Kanye West", "Yeezus", "Genre", "10"], 18),
    (["1996", "Kanye West", "Graduation", "Genre", "10"], 19),
    (["1998", "Björk", "Vespertine", "Genre", "10"], 20),
    (["2014", "Machine Girl", "WLFGRL", "Genre", "10"], 21),
    (["2001", "Hella", "Hold Your Horse Is", "Genre", "10"], 22),
    (["1997", "Don Caballero", "Don Caballero 3", "Genre", "10"], 23),
    (["2000", "Don Caballero", "American Don", "Genre", "10"], 24),
    (["2011", "Don Caballero", "Punkgasm", "Genre", "10"], 25),
]

class BucketListFrame(Frame):
    """
    The frame that contains the list of music that the user has yet to listen to.
    """
    def __init__(self, screen : Screen):
        """Initialize this BucketListFrame."""
        super(BucketListFrame, self).__init__(
            screen=screen,
            height=screen.height,
            width=screen.width,
            has_border=False,
            can_scroll=False,
            name="BucketListFrame"
        )
        self._list = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            columns=["<7", "<30%", "<40%", "<15%"],
            options=test_data,
            titles=["Year", "Artists", "Title", "Genres"],
            name="BucketList",
            add_scroll_bar=True
        )
        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        # TODO: Add text here that shows the keys needed to use the program, perhaps even using colors
        layout1.add_widget(
            Label(label="Q=exit   1=switch to listened list   L=add to listened list   D=add using discogs   M=add manually   X=remove selected   C=credits", align="<", height=1)
        )

        # Set theme that was initialized at the top
        self.set_theme("music-manager")
        # "Initialize" layouts and locations of widgets
        self.fix()

    def find_index_of_entry(self, release_id):
        for index, entry in enumerate(test_data):
            if entry[1] == release_id:
                return index

    def delete_bucket_album(self, release_id : int):
        test_data.pop(release_id)

    def reload_bucket_list(self):
        self._list.options = test_data

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            amount_of_albums = len(self._list.options)

            # Switch to ListenedListTab
            if event.key_code == ord("1"):
                switch_to_tab("ListenedListTab")
            # Show PopUpDialog with credits
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(PopUpDialog(
                    screen=self._screen,
                    text="MusicManager was made by St. K. using Python, asciimatics and the Discogs API.",
                    has_shadow=True,
                    buttons=["Close"],
                ))
            # Delete selected entry from list
            elif event.key_code in [ord("x"), ord("X")] and amount_of_albums > 0:
                self.delete_bucket_album(self.find_index_of_entry(self._list.value))
                self.reload_bucket_list()
            # AddToBucketListDiscogsPopUp
            elif event.key_code in [ord("d"), ord("D")]:
                self._scene.add_effect(AddToBucketListDiscogsPopUp(
                    self._screen
                ))
            # AddToBucketListManuallyPopUp
            elif event.key_code in [ord("m"), ord("M")]:
                self._scene.add_effect(AddToBucketListManuallyPopUp(
                    self._screen, width=self._screen.width * 2 // 3, height=12
                ))
            # AddToListenedListPopUp
            elif event.key_code in [ord("l"), ord("L")] and amount_of_albums > 0:
                self._scene.add_effect(AddToListenedListPopUp(
                    self._screen, album_index=self.find_index_of_entry(self._list.value)
                ))
            # Exit the program
            elif event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                exit_application("Music Manager stopped.")

        return super().process_event(event)

class ListenedListFrame(Frame):
    """
    The frame that contains the list of music that has already been listened to.
    In addition to the expected fields, its table (MultiColumnListBox) also contains
    a "rating" field and a "thoughts" field.
    """
    def __init__(self, screen : Screen):
        """Initialize this ListenedListFrame."""
        super(ListenedListFrame, self).__init__(
            screen=screen,
            height=screen.height,
            width=screen.width,
            has_border=False,
            can_scroll=False,
            name="BucketListFrame"
        )
        self._list = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            columns=["<7", "<30%", "<37%", "<13%", "^12", "^8"],
            options=test_data,
            titles=["Year", "Artists", "Title", "Genres", "Ratings", "Thoughts"],
            name="BucketList",
            add_scroll_bar=True
        )
        layout1 : Layout = Layout(columns=[1], fill_frame=False)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        # TODO: Add text here that shows the keys needed to use the program, perhaps even using colors
        layout1.add_widget(
            Label(label="Q=exit   2=switch bucketlist   E=edit rating & thoughts   X=remove selected   C=credits", align="<", height=1)
        )

        # Set theme that was initialized at the top
        self.set_theme("music-manager")
        # "Initialize" layouts and locations of widgets
        self.fix()

    def find_index_of_entry(self, release_id):
        for index, entry in enumerate(test_data):
            if entry[1] == release_id:
                return index
        pass

    def delete_listened_album(self, release_id : int):
        test_data.pop(release_id)
    
    def reload_listened_list(self):
        self._list.options = test_data

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            amount_of_albums = len(self._list.options)

            # Switch to BucketListTab
            if event.key_code == ord("2"):
                switch_to_tab("BucketListTab")
            # Show PopUpDialog with credits
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(PopUpDialog(
                    screen=self._screen,
                    text="MusicManager was made by St. K. using Python, asciimatics and the Discogs API.",
                    has_shadow=True,
                    buttons=["Close"],
                ))
            # Delete selected entry from list
            elif event.key_code in [ord("x"), ord("X")] and amount_of_albums > 0:
                self.delete_listened_album(self.find_index_of_entry(self._list.value))
                self.reload_listened_list()
            # EditListenedRatingAndThoughtsPopUp
            elif event.key_code in [ord("e"), ord("E")] and amount_of_albums > 0:
                self._scene.add_effect(EditListenedRatingAndThoughtsPopUp(
                    self._screen, album_index=self.find_index_of_entry(self._list.value)
                ))
            # Exit the program
            elif event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                exit_application("Music Manager stopped.")

        return super().process_event(event)

class CustomPopUpBase(Frame):
    """
    Base for my own PopUpDialogs, as the one from Asciimatics isn't sufficient for my needs.
    This base leaves the definiton of Layouts and adding of Widgets to the child classes.
    """
    def __init__(self, screen : Screen, title : str, width : int, height : int):
        # Initialize Frame
        super().__init__(
            screen, height, width, has_shadow=True, is_modal=True, has_border=True, title=title, can_scroll=False,
        )
        # TODO: Currently theme is passable as an argument
        # Perhaps define a separate theme for PopUps
        self.set_theme("default")

    def process_event(self, event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q")]:
                self._close()

        return super().process_event(event)

    def _close(self):
        """Exit out of popup."""
        self._scene.remove_effect(self)

class AddToBucketListDiscogsPopUp(CustomPopUpBase):
    """
    A PopUp to be used for adding releases to the bucketlist using Discogs' search function.
    Should only be instantiated from the BucketListTab.
    It contains a small Text widget for entering a query with a "search" button next to it.
    The result is shown using a Label.
    A "Add" and "Cancel" button are the two options for leaving this PopUp.
    """
    # TODO: Implement a check that makes sure albums aren't being added twice
    def __init__(self, screen : Screen):
        # Initialize CustomPopUpBase
        super().__init__(
            screen, title="Add an album to the bucketlist using Discogs"
        )

        # TODO: Add Widgets for AddToBucketListDiscogsPopUp

        # "Initialize" layouts and locations of widgets
        self.fix()

class AddToBucketListManuallyPopUp(CustomPopUpBase):
    """
    A PopUp to be used for adding albums to the bucketlist by entering release info manually.
    Should only be instantiated from the BucketListTab.
    For this purpose, a form consisting of TextBox / Text widgets is provided.
    A "Add" and "Cancel" button are the two options for leaving this PopUp.
    """
    # TODO: Implement a check that makes sure albums aren't being added twice
    # TODO: Implement a mechanism that creates and checks unique release IDs
    def __init__(self, screen : Screen, width : int, height : int):
        # Initialize CustomPopUpBase
        super().__init__(
            screen, title="Add an album to the bucketlist manually", width=width, height=height
        )

        # TODO: Add Widgets for AddToBucketListManuallyPopUp
        layout1 : Layout = Layout(columns=[1])
        self.add_layout(layout1)
        layout1.add_widget(TextBox(label="Artist(s):", height=3, as_string=True, line_wrap=True))
        layout1.add_widget(TextBox(label="Release Title:", height=3, as_string=True, line_wrap=True))
        layout1.add_widget(Text(label="Year:", validator=check_if_valid_year))
        layout1.add_widget(Text(label="Genre(s):"))
        layout1.add_widget(Divider(draw_line=False))

        layout2 : Layout = Layout(columns=[1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button(text="Add", on_click=self.add_to_bucket_list), column=0)
        layout2.add_widget(Button(text="Cancel", on_click=self._close), column=1)

        # "Initialize" layouts and locations of widgets
        self.fix()

    # TODO: Remove this, perhaps replace with a "global" function somewhere down below
    def add_to_bucket_list(self):
        # TODO: Code to add the entry to the bucketlist
        self._close()
    
    def process_event(self, event):
        """
        Process the events in this PopUp.
        Necessary for the Widgets to work.
        """
        return super().process_event(event)

class AddToListenedListPopUp(CustomPopUpBase):
    """
    A PopUp to be used for moving albums from the bucketlist to the listened list.
    The album's data will be shown.
    Should only be instantiated from the BucketListTab.
    The user can input their rating using a DropdownList and their thoughts using a TextBox.
    A "Add to listened albums" and "Cancel" button are the two options for leaving this PopUp.
    """
    # TODO: Implement a check that makes sure albums aren't being added twice
    def __init__(self, screen : Screen, album_index : int):
        text = "Add '{}' to list of listened albums"
        album_title = test_data[album_index][0][2]

        # Shorten album title incase it's too long
        popup_width = screen.width * 2 // 3
        max_album_length = popup_width - len(text) - 2  # minus 2 to account for the curly braces
        if len(album_title) > max_album_length:
            album_title = album_title[:max_album_length - 3] + "..."

        text = text.format(album_title)

        # Initialize CustomPopUpBase
        super().__init__(
            screen, title=text
        )

        # TODO: Add Widgets for AddToListenedListPopUp

        # "Initialize" layouts and locations of widgets
        self.fix()

class EditListenedRatingAndThoughtsPopUp(CustomPopUpBase):
    """
    A PopUp used for editing the ratings and thoughts for a given album from the listened list.
    Should only be instantiated from the ListenedListTab.
    The user can input their rating using a DropdownList and their thoughts using a TextBox.
    A "Apply change" and "Cancel" button are the two options for leaving this PopUp.
    """
    def __init__(self, screen : Screen, album_index : int):
        text = "Edit rating and thoughts for '" + test_data[album_index][0][2] + "'"
        # Shorten incase of long album title
        popup_width = screen.width * 2 // 3 - 4 # 2 to account for single quotes
        if len(text) > (popup_width):
            text = text[:popup_width - 4] + "...'"
    
        # Initialize CustomPopUpBase
        super().__init__(
            screen, title=text
        )

        # TODO: Add Widgets for EditListenedRatingAndThoughtsPopUp

        # "Initialize" layouts and locations of widgets
        self.fix()

def check_if_valid_year(value : str):
    if len(value) <= 4 and value.isnumeric():
        return True
    else:
        return False

def get_token() -> str:
    """Reads and returns the Discogs API personal access token from the specified file."""
    return open("token.txt", "r").read()

def exit_application(text : str):
    """Exit the program with the given text message."""
    raise StopApplication(message=text)

def switch_to_tab(tab_name : str):
    """Switch to the specified tab (Scene)."""
    raise NextScene(tab_name)

def init_data():
    pass

def generate_random_album_id():
    random_id : str = "".join(random.choices((string.ascii_lowercase + string.ascii_uppercase + string.digits), k=5))
    existing_ids : list[str] = []
    for index, entry in enumerate(test_data):
        existing_ids.append(entry[1])
    
    while random_id in existing_ids:
        random_id = "".join(random.choices((string.ascii_lowercase + string.ascii_uppercase + string.digits), k=5))
    
    return random_id

def enter(screen : Screen, scene : Scene):
    """Entrypoint for the main loop of the program."""
    file_writer = FileWriter()
    file_writer.initialize()
    discogs_helper = DiscogsHelper(get_token())

    scenes = [
        Scene([ListenedListFrame(screen)], duration=-1, name="ListenedListTab"),
        Scene([BucketListFrame(screen)], duration=-1, name="BucketListTab")
    ]
    screen.play(scenes=scenes, stop_on_resize=True, start_scene=scene)