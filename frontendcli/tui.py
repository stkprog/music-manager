from backend.discogs import DiscogsHelper
from backend.files import FileWriter
from backend.models import BucketAlbum, ListenedAlbum

import sys

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, MultiColumnListBox, Widget, Label, PopUpDialog
from asciimatics.event import Event, KeyboardEvent, MouseEvent
from asciimatics.exceptions import NextScene, ResizeScreenError, StopApplication

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
            options=[],
            titles=["Year", "Artists", "Title", "Genres"],
            name="BucketList",
            add_scroll_bar=True
        )
        layout1 = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        # TODO: Add text here that shows the keys needed to use the program, perhaps even using colors
        layout1.add_widget(Label(label="Test", align="<", height=1))

        # "Initialize" layouts and locations of widgets
        self.fix()

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
            elif event.key_code == ord("2"):
                switch_to_tab("BucketListTab")
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(CreditPopUpDialog(self._screen))

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
        layout1.add_widget(Label(label="Test", align="<", height=1))

        # "Initialize" layouts and locations of widgets
        self.fix()

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
            elif event.key_code == ord("2"):
                switch_to_tab("BucketListTab")
            elif event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(CreditPopUpDialog(self._screen))

class CreditPopUpDialog(PopUpDialog):
    def __init__(self, screen : Screen):
        message : str = "MusicManager was made by St. K. using python, asciimatics and the Discogs API."
        super(CreditPopUpDialog, self).__init__(
            screen=screen,
            has_shadow=True,
            buttons=["Ok"],
            text=message,
        )
        # TODO: Nice effect using Stars? Might have to re-implement PopUpDialog for this as well

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