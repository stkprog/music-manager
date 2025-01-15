from backend.models import Album, ListenedAlbum

import os
import json

MUSICMANAGER_PATH : str = os.path.expanduser("~") + "/.music-manager/"

class FileHelper():
    """Utility class for managing local files that hold user data."""

    def __init__(self, list_path : str):
        self.list = []
        self._file_path = MUSICMANAGER_PATH + list_path
        self._ensure_files_exist()
        self._read_list_from_file()

    def _ensure_files_exist(self) -> None:
        """
        Create the .music-manager folder and list files
        and fill it with an empty array if it does not exist yet.
        """
        if not os.path.isdir(MUSICMANAGER_PATH):
            os.mkdir(MUSICMANAGER_PATH)

        if not os.path.exists(self._file_path):
            self.write_to_disk()

    def _read_list_from_file(self) -> None:
        """Read the data from the list file into the list variable."""
        with open(self._file_path, "r", encoding="utf-8") as list_file:
            temp : list = json.load(list_file)
            for t in temp:
                # ** == dictionary unloading
                # values from temp are mapped to class object
                obj : dict = json.loads(t)
                # TypeError if it's a ListenedAlbum
                try:
                    self.list.append(Album(**obj))
                except:
                    self.list.append(ListenedAlbum(**obj))

    def add_new_entry_to_list(self, new_entry : Album) -> None:
        """Add a release to the list if it does not exist yet."""
        for album in self.list:
            if album.release_id == new_entry.release_id:
                return
        self.list.append(new_entry)

    def replace_entry_in_list(self, new_entry : Album) -> None:
        """Replace an entry in the list with a new one."""
        for i in range(len(self.list)):
            if self.list[i].release_id == new_entry.release_id:
                self.list[i] = new_entry

    def remove_entry_from_list(self, release_id : int) -> bool:
        """Remove an entry from the list if it can be found."""
        for i in range(len(self.list)):
            if self.list[i].release_id == release_id:
                self.list.pop(i)
                return True
        return False

    def return_list_as_tuples(self) -> list:
        """
        Return the list in the following formats, depending on if it contains BucketAlbums or ListenedAlbums:
        [([YEAR, ARTISTS, TITLE, GENRES], RELEASE_ID), ([YEAR, ARTISTS, TITLE, GENRES], RELEASE_ID)]
        [([YEAR, ARTISTS, TITLE, GENRES, RATING, THOUGHTS], RELEASE_ID), ([YEAR, ARTISTS, TITLE, GENRES, RATING, THOUGHTS], RELEASE_ID)]
        This format is needed for the options parameter in Asciimatics.
        """
        return [album.return_self_as_tuple() for album in self.list]

    def write_to_disk(self) -> None:
        """
        Write the list content to its file.
        The previous data is overwritten in the process.
        """
        serialized_list = list(map(Album.toJSON, self.list))
        # Use toJSON from Album superclass to convert the list of objects to a list of JSON strings
        with open(self._file_path, "w", encoding="utf-8") as list_file:
            json.dump(serialized_list, list_file)