from backend.discogs import DiscogsHelper
from backend.files import FileWriter
from backend.models import BucketAlbum, ListenedAlbum

import sys

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, MultiColumnListBox, Widget, Label, PopUpDialog, TextBox
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
        layout1 = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        # TODO: Add text here that shows the keys needed to use the program, perhaps even using colors
        layout1.add_widget(
            Label(label="Q=exit   1=switch to listened list   l=add selected to listened list   x=remove selected   c=credits", align="<", height=1)
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
            if event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                exit_application("Music Manager stopped.")
            elif event.key_code == Screen.KEY_F2:
                # TODO: Help dialog showing keys etc.
                pass
            elif event.key_code == ord("1"):
                switch_to_tab("ListenedListTab")
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(CreditPopUpDialog(self._screen))
            elif event.key_code in [ord("l"), ord("L")]:
                # self._scene.add_effect(AddToListenedPopupDialog(self._screen, self._list.value))
                pass
            elif event.key_code in [ord("x"), ord("X")]:
                self.delete_bucket_album(self.find_index_of_entry(self._list.value))
                self.reload_bucket_list()

        return super(BucketListFrame, self).process_event(event)

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
            options=[],
            titles=["Year", "Artists", "Title", "Genres", "Ratings", "Thoughts"],
            name="BucketList",
            add_scroll_bar=True
        )
        layout1 = Layout(columns=[1], fill_frame=False)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        # TODO: Add text here that shows the keys needed to use the program, perhaps even using colors
        layout1.add_widget(
            Label(label="Q=exit   2=switch bucketlist   e=edit rating & thoughts   x=remove selected   c=credits", align="<", height=1)
        )

        # Set theme that was initialized at the top
        self.set_theme("music-manager")
        # "Initialize" layouts and locations of widgets
        self.fix()

    def find_index_of_entry(self, release_id):
        # for index, entry in enumerate(test_data):
        #     if entry[1] == release_id:
        #         return index
        pass

    def delete_listened_album(self, release_id : int):
        # test_data.pop(release_id)
        pass
    
    def reload_listened_list(self):
        # self._list.options = options
        pass

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            if event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                exit_application("Music Manager stopped.")
            elif event.key_code == Screen.KEY_F2:
                # TODO: Help dialog showing keys etc.
                pass
            elif event.key_code == ord("2"):
                switch_to_tab("BucketListTab")
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(CreditPopUpDialog(self._screen))
            elif event.key_code in [ord("X"), ord("X")]:
                self.delete_bucket_album(self.find_index_of_entry(self._list.value))
                self.reload_bucket_list()

        return super(ListenedListFrame, self).process_event(event)

class CreditPopUpDialog(PopUpDialog):
    def __init__(self, screen : Screen):
        message : str = "MusicManager was made by St. K. using python, asciimatics and the Discogs API."
        super(CreditPopUpDialog, self).__init__(
            screen=screen,
            has_shadow=True,
            buttons=["Close"],
            text=message
        )

def get_token() -> str:
    """Reads and returns the Discogs API personal access token from the specified file."""
    return open("token.txt", "r").read()

def exit_application(text : str):
    """Exit the program with the given text message."""
    raise StopApplication(message=text)

def switch_to_tab(tab_name : str):
    """Switch to the specified tab (Scene)."""
    raise NextScene(tab_name)

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