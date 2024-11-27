import os
import json
import typing
from backend.models import Album, BucketAlbum, ListenedAlbum

MM_PATH : str = os.path.expanduser('~') + "/.music-manager"
BUCKET_PATH : str = MM_PATH + "/bucketlist.json"
LISTENED_PATH : str = MM_PATH + "/albums.json"

type BucketList = list[BucketAlbum]
type ListenedList = list[ListenedAlbum]

class FileWriter:
    """Utility class for managing local files that hold user data."""

    def __init__(self):
        self.bucket_list : list[BucketAlbum] = []
        self.listened_list : list[ListenedAlbum] = []

    def _ensure_files_exist(self) -> None:
        """
        Create the .music-manager folder and album and bucket list files
        and fill them with an empty array if they do not exist yet.
        """
        # Make program folder if it doesn't exist
        if not os.path.isdir(MM_PATH):
            os.mkdir(MM_PATH)

        # Create and fill files with empty array if they don't exist
        if not os.path.exists(BUCKET_PATH):
            self.write_to_disk("bucket")
        if not os.path.exists(LISTENED_PATH):
            self.write_to_disk("listened")

    def initialize(self) -> None:
        """Make sure that the program directory and files exist and read the files into memory."""
        self._ensure_files_exist()
        self._read_list_from_file(BUCKET_PATH)
        self._read_list_from_file(LISTENED_PATH)

    def _read_list_from_file(self, file_path : str) -> None:
        """Read the specified file into the appropriate list variable."""
        with open(file_path, "r", encoding="utf-8") as list_file:
            temp : list = json.load(list_file)
            for t in temp:
                # ** == dictionary unloading
                # values from temp are mapped to class object
                obj : dict = json.loads(t)
                if file_path == BUCKET_PATH:
                    self.bucket_list.append(BucketAlbum(**obj))
                elif file_path == LISTENED_PATH:
                    self.listened_list.append(ListenedAlbum(**obj))

    def add_to_list(self, list_to_add_to : list, new_entry : Album) -> None:
        """Add a release to the bucket list if it isn't in the list yet."""
        exists : bool = False
        for release in list_to_add_to:
            if release.release_id == new_entry.release_id:
                exists = True
                break
        if not exists:
            list_to_add_to.append(new_entry)

    def edit_entry_in_listened_list(self, release_id_to_edit : int, new_rating : int, new_thoughts : str) -> None:
        """Edit the rating and / or thoughts of a release if it can be found in the listened list."""
        for a in self.listened_list:
            if a.release_id == release_id_to_edit:
                a.rating = new_rating
                a.thoughts = new_thoughts
                break

    def remove_from_list(self, list_to_delete_from : list, release_id : int) -> None:
        """Remove a release from the specified list if it can be found in that list."""
        for i in range(len(list_to_delete_from)):
            if list_to_delete_from[i].release_id == release_id:
                list_to_delete_from.pop(i)
                break

    # TODO: Find a solution that doesn't require using an extra utility variable
    # for checking which list to use, because this isn't ideal
    def write_to_disk(self, which_list : str) -> None:
        """
        Write the specified list to its appropriate file.
        The previous data is overwritten in the process.
        """
        file_path : str = ""
        list_to_write : list[Album] = []
        if which_list == "bucket":
            file_path = BUCKET_PATH
            list_to_write = self.bucket_list
        elif which_list == "listened":
            file_path = LISTENED_PATH
            list_to_write = self.listened_list

        # Use toJSON from Album superclass to convert the list of objects to a list of JSON strings
        serialized_list = list(map(Album.toJSON, list_to_write))

        with open(file_path, "w", encoding="utf-8") as list_file:
            json.dump(serialized_list, list_file)