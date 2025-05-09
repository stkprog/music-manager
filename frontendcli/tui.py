from backend.discogs import DiscogsHelper
from backend.filehelper import FileHelper
from backend.filehelper import MUSICMANAGER_PATH
from backend.models import Album, BucketAlbum, ListenedAlbum

import string
import random

from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Button, MultiColumnListBox, Widget, Label, PopUpDialog, TextBox, Text, Divider, DropdownList
from asciimatics.widgets.utilities import THEMES
from asciimatics.event import Event, KeyboardEvent
from asciimatics.exceptions import NextScene, StopApplication

# Initialize helper objects to be used in this script
b_filehelper = FileHelper(list_path="bucketlist.json")
l_filehelper = FileHelper(list_path="listenedlist.json")
discogs_helper = DiscogsHelper(DiscogsHelper.read_personal_access_token())

THEMES["music-manager"] = {
    #                   FOREGROUND                          ATTRIBUTE           BACKGROUND
    "background": (Screen.COLOUR_WHITE,                 Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "shadow": (Screen.COLOUR_BLACK,                     None,               Screen.COLOUR_BLACK),
    "disabled": (Screen.COLOUR_BLACK,                   Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "invalid": (Screen.COLOUR_YELLOW,                   Screen.A_BOLD,      Screen.COLOUR_RED),
    "label": (Screen.COLOUR_BLACK,                      Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "borders": (Screen.COLOUR_WHITE,                    Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "scroll": (Screen.COLOUR_WHITE,                     Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "title": (Screen.COLOUR_BLACK,                      Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "edit_text": (Screen.COLOUR_BLACK,                  Screen.A_BOLD,      Screen.COLOUR_WHITE),
    "focus_edit_text": (Screen.COLOUR_BLACK,            Screen.A_NORMAL,    Screen.COLOUR_WHITE),
    "readonly": (Screen.COLOUR_BLUE,                    Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "focus_readonly": (Screen.COLOUR_YELLOW,            Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "button": (Screen.COLOUR_WHITE,                     Screen.A_NORMAL,    Screen.COLOUR_BLUE),
    "focus_button": (Screen.COLOUR_WHITE,               Screen.A_BOLD,      Screen.COLOUR_CYAN),
    "control": (Screen.COLOUR_CYAN,                     Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_control": (Screen.COLOUR_CYAN,            Screen.A_BOLD,      Screen.COLOUR_BLUE),
    "focus_control": (Screen.COLOUR_CYAN,               Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_focus_control": (Screen.COLOUR_CYAN,      Screen.A_BOLD,      Screen.COLOUR_BLACK),
    "field": (Screen.COLOUR_WHITE,                      Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_field": (Screen.COLOUR_WHITE,             Screen.A_NORMAL,    Screen.COLOUR_BLUE),
    "focus_field": (Screen.COLOUR_WHITE,                Screen.A_NORMAL,    Screen.COLOUR_BLACK),
    "selected_focus_field": (Screen.COLOUR_WHITE,       Screen.A_BOLD,      Screen.COLOUR_BLUE),
    "selected_sort_label": (Screen.COLOUR_CYAN,        Screen.A_BOLD,      Screen.COLOUR_BLACK),
}
THEMES["default"]["label"] = (Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_BLUE)

# Just for reference

# test_bucketlist = [
#     (["2024", "Machine Girl", "MG Ultra", "Electronic"], 1243465),
#     (["2018", "Machine Girl", "The Ugly Art", "Electronic"], 1),
#     (["2002", "Boards of Canada", "Music Has the Right to Children", "Genre"], 2),
#     (["2017", "Machine Girl", "...Because I'm Young Arrogant and Hate Everything You Stand For", "Genre"], 3),
#     (["2015", "Machine Girl", "Gemini", "Genre"], 4),
#     (["2018", "Machine Girl", "The Ugly Art", "Genre"], 5),
#     (["2020", "Machine Girl", "U-Void Synthesizer", "Genre"], 6),
#     (["2023", "Black Midi", "Hellfire", "Genre"], 7),
#     (["2022", "Black Midi", "Cavalcade", "Genre"], 8),
#     (["2021", "Black Midi", "Schlagenheim", "Genre"], 9),
#     (["2002", "Madvillain", "Madvillainy", "Genre"], 10),
# ]

# test_listenedlist = [
#     (["2002", "Boards of Canada", "Geogaddi", "Genre", "10", "my thoughts"], 11),
#     (["2003", "Aphex Twin", "Druqks", "Genre", "10", "my thoughts"], 12),
#     (["1999", "Aphex Twin", "Selected Ambient Works", "Genre", "10", "my thoughts"], 13),
#     (["1970", "Radiohead", "In Rainbows", "Genre", "10", "my thoughts"], 14),
#     (["1996", "Radiohead", "OK Computer", "Genre", "10", "my thoughts"], 15),
#     (["????", "King Crimson", "Red", "Genre", "10", "my thoughts"], 16),
#     (["1981", "King Crimson", "In the Hall of the Crimson King", "Genre", "10", "my thoughts"], 17),
#     (["2000", "Kanye West", "Yeezus", "Genre", "10", "my thoughts"], 18),
#     (["1996", "Kanye West", "Graduation", "Genre", "10", "my thoughts"], 19),
#     (["1998", "Björk", "Vespertine", "Genre", "10", "my thoughts"], 20),
#     (["2014", "Machine Girl", "WLFGRL", "Genre", "10", "my thoughts"], 21),
#     (["2001", "Hella", "Hold Your Horse Is", "Genre", "10", "my thoughts"], 22),
#     (["1997", "Don Caballero", "Don Caballero 3", "Genre", "10", "my thoughts"], 23),
#     (["2000", "Don Caballero", "American Don", "Genre", "10", "my thoughts"], 24),
#     (["2011", "Don Caballero", "Punkgasm", "Genre", "10", "my thoughts"], 25),
# ]

class CustomTabBase(Frame):
    """A base class for the two 'tabs' that the user switches to and from."""
    
    def __init__(self, screen : Screen, mclistbox : MultiColumnListBox, file_helper : FileHelper):
        super().__init__(
            screen,
            width=screen.width,
            height=screen.height,
            has_border=False,
            can_scroll=False
        )
        self._file_helper = file_helper
        self._list = mclistbox
        self.set_theme("music-manager")
        self._sort_reverse = False

        self._sort_by_year_label = Label(label="F2=year", align="^", height=1)
        self._sort_by_artists_label = Label(label="F3=artist(s)", align="^", height=1)
        self._sort_by_title_label = Label(label="F4=title", align="^", height=1)
        self._sort_by_genres_label = Label(label="F5=genre(s)", align="^", height=1)

    def find_index_of_entry(self, release_id : int) -> int:
        """Takes a release_id and searches for the corresponding album in this Tab's list."""
        for index, entry in enumerate(self._list.options):
            if entry[1] == release_id:
                return index

    def _find_current_entry(self) -> Album:
        """Returns the current entry selected in the MultiColumnListBox."""
        return self._file_helper.list[self.find_index_of_entry(self._list.value)]

    def _reverse_sorting_order(self) -> None:
        """Reverses the boolean handling the sorting order."""
        self._sort_reverse = not self._sort_reverse

    def _delete_release_from_list(self, release_id : int) -> None:
        """Deletes an album from the specified list."""
        self._file_helper.remove_entry_from_list(release_id)

    def _reload_list(self) -> None:
        """The updated list is loaded into this Tab's list again."""
        self._list.options = self._file_helper.return_list_as_tuples()

    def _reset_sort_labels(self):
        """
        Reset all the labels used for showing the current sort mode.
        This includes setting their text back to normal and the color palette to the normal "label" one.
        """
        self._sort_by_year_label.text = "F2=year"
        self._sort_by_year_label.custom_colour = None
        self._sort_by_artists_label.text = "F3=artist(s)"
        self._sort_by_artists_label.custom_colour = None
        self._sort_by_title_label.text = "F4=title"
        self._sort_by_title_label.custom_colour = None
        self._sort_by_genres_label.text = "F5=genre(s)"
        self._sort_by_genres_label.custom_colour = None

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            
            # Show PopUpDialog with credits
            if event.key_code in [ord("c"), ord("C")]:
                self._scene.add_effect(PopUpDialog(
                    screen=self._screen,
                    text="MusicManager was made by St. K. using Python, asciimatics and the Discogs API.",
                    has_shadow=True,
                    buttons=["Close"],
                ))
            # Sort by Year
            elif event.key_code == Screen.KEY_F2:
                self._file_helper.list = sorted(self._file_helper.list, key=lambda album:album.year, reverse=self._sort_reverse)
                self._reset_sort_labels()
                self._sort_by_year_label.custom_colour = "selected_sort_label"
                self._sort_by_year_label.text += " ▼" if self._sort_reverse else " ▲"
                self._reverse_sorting_order()
                self._reload_list()
            # Sort by Artist(s)
            elif event.key_code == Screen.KEY_F3:
                self._file_helper.list = sorted(self._file_helper.list, key=lambda album:album.artists, reverse=self._sort_reverse)
                self._reset_sort_labels()
                self._sort_by_artists_label.custom_colour = "selected_sort_label"
                self._sort_by_artists_label.text += " ▼" if self._sort_reverse else " ▲"
                self._reverse_sorting_order()
                self._reload_list()
            # Sort by Title
            elif event.key_code == Screen.KEY_F4:
                self._file_helper.list = sorted(self._file_helper.list, key=lambda album:album.title, reverse=self._sort_reverse)
                self._reset_sort_labels()
                self._sort_by_title_label.custom_colour = "selected_sort_label"
                self._sort_by_title_label.text += " ▼" if self._sort_reverse else " ▲"
                self._reverse_sorting_order()
                self._reload_list()
            # Sort by Genres
            elif event.key_code == Screen.KEY_F5:
                self._file_helper.list = sorted(self._file_helper.list, key=lambda album:album.genres, reverse=self._sort_reverse)
                self._reset_sort_labels()
                self._sort_by_genres_label.custom_colour = "selected_sort_label"
                self._sort_by_genres_label.text += " ▼" if self._sort_reverse else " ▲"
                self._reverse_sorting_order()
                self._reload_list()
            # Delete selected entry from list
            elif event.key_code in [ord("x"), ord("X")] and len(self._list.options) > 0:
                # self._delete_release_from_list(self._list.value)
                # self._file_helper.write_to_disk()
                # self._reload_list()
                self._scene.add_effect(ReallyDeleteFromListPopUp(
                    screen=self.screen,
                    album=self._find_current_entry(),
                    file_helper=self._file_helper,
                    parent_frame=self
                ))
            # Exit the program
            elif event.key_code in [ord("q"), ord("Q"), Screen.ctrl("c")]:
                exit_application("Music Manager stopped.")

        # Other processing is handled in parent class
        return super().process_event(event)

class BucketListFrame(CustomTabBase):
    """The frame that contains the list of music that the user has yet to listen to."""

    def __init__(self, screen : Screen, file_helper : FileHelper):
        """Initialize this BucketListFrame."""
        mclistbox = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            columns=["<6", "<30%", "0", "<25%"],
            options=file_helper.return_list_as_tuples(),
            titles=["Year", "Artist(s)", "Title", "Genre(s)"],
            name="BucketList",
            add_scroll_bar=True
        )
        super().__init__(
            screen=screen,
            mclistbox=mclistbox,
            file_helper=file_helper
        )
        
        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout=layout1)
        layout1.add_widget(self._list)
        layout1.add_widget(Label(
            label="Q=exit   1=listened list   L=add to listened list   D=add using discogs   M=add manually   X=remove   C=credits",
            align="<",
            height=1
        ))

        layout2 : Layout = Layout(columns=[1, 1, 1, 1, 1], fill_frame=False, gutter=0)
        self.add_layout(layout2)
        layout2.add_widget(Label(label="Sorting:", align="<", height=1), 0)
        layout2.add_widget(self._sort_by_year_label, 1)
        layout2.add_widget(self._sort_by_artists_label, 2)
        layout2.add_widget(self._sort_by_title_label, 3)
        layout2.add_widget(self._sort_by_genres_label, 4)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            amount_of_albums = len(self._list.options)

            # Switch to ListenedListTab
            if event.key_code == ord("1"):
                switch_to_tab("ListenedListTab")
            # AddToBucketListDiscogsPopUp
            elif event.key_code in [ord("d"), ord("D")]:
                self._scene.add_effect(AddToBucketListDiscogsPopUp(
                    screen=self._screen, file_helper=b_filehelper, parent_frame=self
                ))
            # AddToBucketListManuallyPopUp
            elif event.key_code in [ord("m"), ord("M")]:
                self._scene.add_effect(AddToBucketListManuallyPopUp(
                    screen=self._screen, file_helper=b_filehelper, parent_frame=self
                ))
            # AddToListenedListPopUp
            elif event.key_code in [ord("l"), ord("L")] and amount_of_albums > 0:
                album = self._find_current_entry()
                self._scene.add_effect(AddToListenedListPopUp(
                    screen=self._screen, album=album, b_filehelper=b_filehelper, l_filehelper=l_filehelper, parent_frame=self
                ))

        # Other processing is handled in parent class
        return super().process_event(event)

class ListenedListFrame(CustomTabBase):
    """
    The frame that contains the list of music that has already been listened to.
    In addition to the expected fields, its table (MultiColumnListBox) also contains
    a "rating" field and a "thoughts" field.
    """

    def __init__(self, screen : Screen, file_helper : FileHelper):
        """Initialize this ListenedListFrame."""
        mclistbox = MultiColumnListBox(
            height=Widget.FILL_FRAME,
            columns=["<6", "<30%", "0", "<20%", "^12", "^8"],
            options=file_helper.return_list_as_tuples(),
            titles=["Year", "Artist(s)", "Title", "Genre(s)", "Ratings", "Thoughts"],
            name="ListenedList",
            add_scroll_bar=True
        )
        super().__init__(
            screen=screen,
            mclistbox=mclistbox,
            file_helper=file_helper
        )

        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(self._list)
        layout1.add_widget(Label(
            label="Q=exit   2=bucketlist   E=edit rating & thoughts   T=view thoughts   X=remove   C=credits", align="<", height=1
        ))

        layout2 : Layout = Layout(columns=[1, 1, 1, 1, 1, 1], fill_frame=False, gutter=0)
        self.add_layout(layout2)
        layout2.add_widget(Label(label="Sorting:", align="<", height=1), 0)
        self._sort_by_rating_label = Label(label="F6=rating", align="^", height=1)
        layout2.add_widget(self._sort_by_year_label, 1)
        layout2.add_widget(self._sort_by_artists_label, 2)
        layout2.add_widget(self._sort_by_title_label, 3)
        layout2.add_widget(self._sort_by_genres_label, 4)
        layout2.add_widget(self._sort_by_rating_label, 5)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _reset_sort_labels(self):
        """
        Reset all the labels used for showing the current sort mode.
        This includes setting their text back to normal and the color palette to the normal "label" one.
        """
        super()._reset_sort_labels()
        self._sort_by_rating_label.text = "F6=rating"
        self._sort_by_rating_label.custom_colour = None

    def process_event(self, event : Event):
        """Do the key handling for this Frame."""
        if isinstance(event, KeyboardEvent):
            amount_of_albums = len(self._list.options)

            # Switch to BucketListTab
            if event.key_code == ord("2"):
                switch_to_tab("BucketListTab")
            # Sort by Rating
            elif event.key_code == Screen.KEY_F6:
                self._file_helper.list = sorted(self._file_helper.list, key=lambda album:album.rating, reverse=self._sort_reverse)
                self._reset_sort_labels()
                self._sort_by_rating_label.custom_colour = "selected_sort_label"
                self._sort_by_rating_label.text += " ▼" if self._sort_reverse else " ▲"
                self._reverse_sorting_order()
                self._reload_list()
            # EditListenedRatingAndThoughtsPopUp
            elif event.key_code in [ord("e"), ord("E")] and amount_of_albums > 0:
                self._scene.add_effect(EditListenedRatingAndThoughtsPopUp(
                    self._screen, album=self._find_current_entry(), file_helper=l_filehelper, parent_frame=self
                ))
            elif event.key_code in [ord("t"), ord("E")] and amount_of_albums > 0:
                self._scene.add_effect(ViewThoughtsPopUp(
                    self._screen, 
                    album_title=self._find_current_entry().title, 
                    album_thoughts=self._find_current_entry().thoughts, 
                    parent_frame=self
                ))

        # Other processing is handled in parent class
        return super().process_event(event)

class CustomPopUpBase(Frame):
    """
    Base for my own PopUpDialogs, as the one from Asciimatics isn't sufficient for my needs.
    This base leaves the definiton of Layouts and adding of Widgets to the child classes.
    """

    def __init__(self, screen : Screen, title : str, width : int, height : int, parent_frame : CustomTabBase):
        # Initialize Frame
        super().__init__(
            screen, height, width, has_shadow=True, is_modal=False, has_border=True, title=title, can_scroll=False
        )
        self._parent_frame = parent_frame
        self.set_theme("default")

    def process_event(self, event):
        """Do the key handling for this Frame."""
        # Other processing is handled in parent class
        return super().process_event(event)

    def _close(self) -> None:
        """Exit out of this PopUp."""
        self._parent_frame._reload_list()
        self._scene.remove_effect(self)

class AddToBucketListDiscogsPopUp(CustomPopUpBase):
    """
    A PopUp to be used for adding releases to the bucketlist using Discogs' search function.
    Should only be instantiated from the BucketListTab.
    It contains a small Text widget for entering a query with a "search" button next to it.
    The result is shown using a Label.
    A "Add" and "Cancel" button are the two options for leaving this PopUp.
    """

    def __init__(self, screen : Screen, file_helper : FileHelper, parent_frame : BucketListFrame):
        # Initialize CustomPopUpBase
        super().__init__(
            screen,
            title="Add an album to the bucketlist using Discogs",
            width=screen.width * 4 // 5,
            height=8,
            parent_frame=parent_frame
        )
        self._file_helper = file_helper

        divider = Divider(draw_line=False, height=1)

        # Create Layouts and Widgets
        layout1 : Layout = Layout(columns=[screen.width * 4 // 5 - 14, 18])
        self.add_layout(layout1)
        layout1.add_widget(divider, 0)
        layout1.add_widget(divider, 1)
        self._text = layout1.add_widget(Text(), 0)
        layout1.add_widget(Button("Search", on_click=self._search), 1)

        layout2 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout2)
        layout2.add_widget(divider)
        self._result_label = layout2.add_widget(Label("", height=1))
        layout2.add_widget(divider)

        layout3 : Layout = Layout(columns=[1, 1, 1])
        self.add_layout(layout3)
        self._add_button = layout3.add_widget(Button("Add", on_click=self._add_to_bucket_list), 0)
        self._add_button.disabled = True
        self._redo_button = layout3.add_widget(Button("Redo", on_click=self._redo_search), 1)
        self._redo_button.disabled = True
        layout3.add_widget(Button("Cancel", on_click=self._close), 2)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _add_to_bucket_list(self) -> None:
        """Add the found album to the bucketlist."""
        if self._result != None and not self._new_entry_already_exists(self._result):
            self._file_helper.add_new_entry_to_list(self._result)
            self._file_helper.write_to_disk()
            self._close()
    
    def _new_entry_already_exists(self, new_entry : BucketAlbum) -> bool:
        """Checks if the new entry is already in the list."""
        for entry in self._file_helper.list:
            if new_entry.release_id == entry.release_id:
                return True
        return False

    def _redo_search(self, message="") -> None:
        """Reset the Widgets in the PopUp."""
        self._result = None
        self._text.value = ""
        self._result_label.text = ""
        self._add_button.disabled = True
        self._redo_button.disabled = True
        # Switch focus back to Text element
        self.switch_focus(layout=self._layouts[0], column=0, widget=1)

    def _search(self) -> None:
        """Search for an album on Discogs using the user's entered query and present the results."""
        self._redo_button.disabled = False
        
        # No user query
        if self._text.value == "":
            # Switch focus to "Redo" button
            self.switch_focus(layout=self._layouts[2], column=1, widget=0)
            self._result_label.text = "Must enter a search term"
            return
        
        # User query given
        self._result = discogs_helper.search_one(user_query=self._text.value)
        # No result found
        if self._result == None:
            self._result_label.text = "Album not found"
            # Switch focus to "Redo" button
            self.switch_focus(layout=self._layouts[2], column=1, widget=0)
            return
        
        # Result found
        # Result already in list
        if self._new_entry_already_exists(self._result):
            self._add_button.disabled = True
            self._result_label.text = "{} - Album is already in list".format(self._result.title)
            # Switch focus to "Redo" button
            self.switch_focus(layout=self._layouts[2], column=1, widget=0)
        # Result is new
        else:
            self._result_label.text = "{} - {} ({}) [{}]".format(
                self._result.artists, self._result.title, self._result.year ,self._result.genres
            )
            self._add_button.disabled = False
            # Focus to "Add" button
            self.switch_focus(layout=self._layouts[2], column=0, widget=0)

    def process_event(self, event):
        """Do the key handling for this Frame."""
        return super().process_event(event)

class AddToBucketListManuallyPopUp(CustomPopUpBase):
    """
    A PopUp to be used for adding albums to the bucketlist by entering release info manually.
    Should only be instantiated from the BucketListTab.
    For this purpose, a form consisting of TextBox / Text widgets is provided.
    A "Add" and "Cancel" button are the two options for leaving this PopUp.
    """

    def __init__(self, screen : Screen, file_helper : FileHelper, parent_frame : BucketListFrame):
        # Initialize CustomPopUpBase
        super().__init__(
            screen,
            title="Add an album to the bucketlist manually",
            width=screen.width * 4 // 5,
            height=11,
            parent_frame=parent_frame
        )
        self._file_helper = file_helper

        divider = Divider(draw_line=False, height=1)

        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(divider)
        self._input_artists = layout1.add_widget(Text(label="Artist(s):", validator=self._check_if_string_not_none))
        self._input_title = layout1.add_widget(Text(label="Release Title:", validator=self._check_if_string_not_none))
        self._input_year = layout1.add_widget(Text(label="Year:", validator=self._check_if_valid_year))
        self._input_genres = layout1.add_widget(Text(label="Genre(s):", validator=self._check_if_string_not_none))
        layout1.add_widget(divider)

        layout2 : Layout = Layout(columns=[1])
        self.add_layout(layout2)
        self._error_label = layout2.add_widget(Label("", height=1))
        layout2.add_widget(divider)
        self._errors = []

        layout3 : Layout = Layout(columns=[1, 1, 1, 1])
        self.add_layout(layout3)
        layout3.add_widget(Button(text="Add", on_click=self._add_to_bucket_list), 1)
        layout3.add_widget(Button(text="Cancel", on_click=self._close), 2)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _add_to_bucket_list(self) -> None:
        """Uses the data entered by the user to add a new entry to the bucketlist."""
        # Reset errors list
        self._errors = []
        
        if self._all_inputs_valid():
            new_bucket = BucketAlbum(
                release_id=self._generate_random_release_id(),
                artists=self._input_artists.value,
                title=self._input_title.value,
                year=self._input_year.value,
                genres=self._input_genres.value
            )
            self._file_helper.add_new_entry_to_list(new_bucket)
            self._file_helper.write_to_disk()
            self._close()
        else:
            self._error_label.text = ", ".join(self._errors).capitalize() + "."
    
    def _generate_random_release_id(self) -> int:
        """Utility method for generating a random release_id for a manually added album."""
        # Generate a random long integer
        random_id : int = int("".join(random.choices((string.digits), k=14)))
        existing_ids : list[int] = []
        for index, entry in enumerate(self._file_helper.list):
            existing_ids.append(entry.release_id)
        
        while random_id in existing_ids:
            random_id = int("".join(random.choices((string.digits), k=14)))
        
        return random_id

    def _all_inputs_valid(self) -> bool:
        """
        Checks if all the user inputs are valid.
        Adds errors for UI output.
        """
        if not self._input_artists.is_valid:
            self._errors.append("No artist(s) given")
        if not self._input_title.is_valid:
            self._errors.append("no title given")
        if not self._input_year.is_valid:
            self._errors.append("year must be a number")
        if not self._input_genres.is_valid:
            self._errors.append("no genre(s) given")
        
        return self._input_artists.is_valid and self._input_title.is_valid and self._input_year.is_valid and self._input_genres.is_valid

    def _check_if_valid_year(self, value : str) -> bool:
        """Ensures that a year entered by the user is 4 digits or less and consists only of digits."""
        if len(value) <= 4 and value.isnumeric():
            return True
        else:
            return False
    
    def _check_if_string_not_none(self, value : str) -> bool:
        """Ensures that a given string is not None or empty."""
        return value != None and value != ""

    def process_event(self, event):
        """Do the key handling for this Frame."""
        return super().process_event(event)

class AddToListenedListPopUp(CustomPopUpBase):
    """
    A PopUp to be used for moving albums from the bucketlist to the listened list.
    The album's data will be shown.
    Should only be instantiated from the BucketListTab.
    The user can input their rating using a DropdownList and their thoughts using a TextBox.
    A "Add to listened albums" and "Cancel" button are the two options for leaving this PopUp.
    """

    def __init__(
            self, screen : Screen, album : BucketAlbum, b_filehelper : FileHelper, l_filehelper : FileHelper, parent_frame : BucketListFrame
        ):
        self._b_filehelper = b_filehelper
        self._l_filehelper = l_filehelper
    
        text = "Add '{}' to list of listened albums"
        self._bucket_album : BucketAlbum = album
        album_title = self._bucket_album.title

        # Shorten album title incase it's too long
        popup_width = screen.width * 4 // 5
        max_album_length = popup_width - len(text) - 2  # minus 2 to account for the curly braces
        if len(album_title) > max_album_length:
            album_title = album_title[:max_album_length - 3] + "..."

        text = text.format(album_title)

        # Initialize CustomPopUpBase
        super().__init__(
            screen, title=text, width=popup_width, height=15, parent_frame=parent_frame
        )

        divider = Divider(draw_line=False, height=1)

        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(divider)
        self._album_artists = layout1.add_widget(Text(label="Artist(s):"))
        self._album_artists.disabled = True
        self._album_artists.value = self._bucket_album.artists
        self._album_title = layout1.add_widget(Text(label="Release Title:"))
        self._album_title.disabled = True
        self._album_title.value = self._bucket_album.title
        self._album_year = layout1.add_widget(Text(label="Year:"))
        self._album_year.value = self._bucket_album.year
        self._album_year.disabled = True
        self._album_genres = layout1.add_widget(Text(label="Genre(s):"))
        self._album_genres.value = self._bucket_album.genres
        self._album_genres.disabled = True

        layout1.add_widget(divider)
        self._album_rating = layout1.add_widget(DropdownList(
            # 1 to 10
            options=tuple([str(i + 1), i + 1] for i in range(10)),
            label="Rating",
            fit=True
        ))
        self._album_thoughts = layout1.add_widget(TextBox(label="Thoughts:", as_string=True, height=5))

        layout2 = Layout(columns=[1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", on_click=self._move_from_bucket_to_listened_list), 0)
        layout2.add_widget(Button("Cancel", on_click=self._close), 1)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _move_from_bucket_to_listened_list(self):
        """Deletes the new entry from the bucketlist and adds it to the listened list."""
        listened_album = ListenedAlbum(
            self._bucket_album.release_id,
            self._bucket_album.artists,
            self._bucket_album.title,
            self._bucket_album.genres,
            self._bucket_album.year,
            str(self._album_rating.value),
            self._album_thoughts.value
        )
        self._b_filehelper.remove_entry_from_list(self._bucket_album.release_id)
        self._b_filehelper.write_to_disk()
        self._l_filehelper.add_new_entry_to_list(listened_album)
        self._l_filehelper.write_to_disk()
        self._close()

    def _close(self) -> None:
        """
        Exit out of this PopUp.
        Polymorphism to account for two parent frames.
        """
        """Exit out of this PopUp."""
        self._parent_frame._reload_list()
        # This is a bit unfortunate. Reloading ListenedListTab
        self._screen._scenes[1].effects[0]._reload_list()
        self._scene.remove_effect(self)

    def process_event(self, event):
        """Do the key handling for this Frame."""
        return super().process_event(event)

class EditListenedRatingAndThoughtsPopUp(CustomPopUpBase):
    """
    A PopUp used for editing the ratings and thoughts for a given album from the listened list.
    Should only be instantiated from the ListenedListTab.
    The user can input their rating using a DropdownList and their thoughts using a TextBox.
    A "Apply change" and "Cancel" button are the two options for leaving this PopUp.
    """

    def __init__(self, screen : Screen, album : ListenedAlbum, file_helper : FileHelper, parent_frame : ListenedListFrame):
        self._file_helper = file_helper
    
        self._listened_album : ListenedAlbum = album
        text = "Edit rating and thoughts for '" + self._listened_album.title + "'"
        # Shorten incase of long album title
        popup_width = screen.width * 4 // 5 - 4 # minus 4 to account for quotes
        if len(text) > (popup_width):
            text = text[:popup_width - 4] + "...'"
    
        # Initialize CustomPopUpBase
        super().__init__(
            screen, title=text, width=popup_width, height=15, parent_frame=parent_frame
        )

        divider = Divider(draw_line=False, height=1)

        layout1 : Layout = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(divider)
        self._album_artists = layout1.add_widget(Text(label="Artist(s):"))
        self._album_artists.disabled = True
        self._album_artists.value = self._listened_album.artists
        self._album_title = layout1.add_widget(Text(label="Release Title:"))
        self._album_title.disabled = True
        self._album_title.value = self._listened_album.title
        self._album_year = layout1.add_widget(Text(label="Year:"))
        self._album_year.value = self._listened_album.year
        self._album_year.disabled = True
        self._album_genres = layout1.add_widget(Text(label="Genre(s):"))
        self._album_genres.value = self._listened_album.genres
        self._album_genres.disabled = True
        
        layout1.add_widget(divider)
        self._album_rating = layout1.add_widget(DropdownList(
            # 1 to 10
            options=tuple([str(i + 1), i + 1] for i in range(10)),
            label="Rating",
            fit=True
        ))
        self._album_rating.value = int(self._listened_album.rating)
        self._album_thoughts = layout1.add_widget(TextBox(label="Thoughts:", as_string=True, height=5))
        self._album_thoughts.value = self._listened_album.thoughts

        layout2 = Layout(columns=[1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Change", on_click=self._change_rating_and_thoughts), 0)
        layout2.add_widget(Button("Cancel", on_click=self._close), 1)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _change_rating_and_thoughts(self) -> None:
        """Replace the old listened album with the new one, which has the updated rating and thoughts."""
        listened_album = ListenedAlbum(
            self._listened_album.release_id,
            self._listened_album.artists,
            self._listened_album.title,
            self._listened_album.genres,
            self._listened_album.year,
            str(self._album_rating.value),
            self._album_thoughts.value
        )
        self._file_helper.replace_entry_in_list(new_entry=listened_album)
        self._file_helper.write_to_disk()
        self._close()

    def process_event(self, event):
        """Do the key handling for this Frame."""
        return super().process_event(event)

class ViewThoughtsPopUp(CustomPopUpBase):
    """A simple PopUp for viewing the user's thoughts about the currently selected listened album."""
    def __init__(self, screen : Screen, album_title : str, album_thoughts : str, parent_frame : ListenedListFrame):
        text = "Thoughts on '" + album_title + "'"
        # Shorten incase of long album title
        popup_width = screen.width * 3 // 4 - 4     # minus 4 to account for quotes
        if len(text) > (popup_width):
            text = text[:popup_width - 4] + "...'"

        super().__init__(
            screen, title=text, width=popup_width, height=screen.height * 3 // 4, parent_frame=parent_frame
        )

        divider = Divider(draw_line=False, height=1)

        layout1 = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(divider)
        popup_height = screen.height * 3 // 4 - 2   # minus 2 to account for borders
        textbox_height = popup_height - 3           # minus 3 to account for dividers and closing button 
        self._album_thoughts = layout1.add_widget(TextBox(as_string=True, height=textbox_height, line_wrap=True, readonly=True))
        self._album_thoughts.value = album_thoughts
        layout1.add_widget(divider)
        
        layout2 = Layout(columns=[1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Close", on_click=self._close))

        # "Initialize" layouts and locations of widgets
        self.fix()

class ReallyDeleteFromListPopUp(CustomPopUpBase):
    """A PopUp asking the user for confirmation to delete the selected entry."""
    def __init__(self, screen : Screen, album : ListenedAlbum, file_helper : FileHelper, parent_frame : ListenedListFrame):
        super().__init__(
            screen, title="Confirm Deletion", width=screen.width * 1 // 2, height=screen.height * 1 // 2, parent_frame=parent_frame
        )

        self._album : Album = album
        self._file_helper : FileHelper = file_helper

        layout1 = Layout(columns=[1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(
            Label(label="Really delete '" + self._album.title + "' from the list?", height=5)
        )

        layout2 = Layout(columns=[1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Delete", on_click=self._delete_album_from_list), 0)
        layout2.add_widget(Button("Cancel", on_click=self._close), 1)

        # "Initialize" layouts and locations of widgets
        self.fix()

    def _delete_album_from_list(self):
        """If user confirmed deletion, remove the entry from the list and write to file."""
        self._file_helper.remove_entry_from_list(release_id=self._album.release_id)
        self._file_helper.write_to_disk()
        self._close()
    
    def process_event(self, event):
        """Do the key handling for this Frame."""
        return super().process_event(event)

def exit_application(text : str) -> None:
    """Exit the program with the given text message."""
    raise StopApplication(message=text)

def switch_to_tab(tab_name : str) -> None:
    """Switch to the specified Tab (Scene)."""
    raise NextScene(tab_name)

def enter(screen : Screen, scene : Scene) -> None:
    """Entrypoint for the main loop of the program."""
    scenes = [
        Scene(
            [BucketListFrame(screen, file_helper=b_filehelper)], duration=-1, name="BucketListTab"
        ),
        Scene(
            [ListenedListFrame(screen, file_helper=l_filehelper)], duration=-1, name="ListenedListTab"
        )
    ]
    screen.play(scenes=scenes, stop_on_resize=True, start_scene=scene)

    # Save any list changes to disk
    b_filehelper.write_to_disk()
    l_filehelper.write_to_disk()