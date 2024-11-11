import os
import json
from backend.models import Listened

MM_PATH : str = os.path.expanduser('~') + "/.music-manager"
BUCKET_PATH : str = MM_PATH + "/bucketlist.txt"
ALBUM_PATH : str = MM_PATH + "/albums.txt"

class FileWriter:
    def __init__(self):
        self.bucket_list : list = []
        self.album_list : list = []

    def ensure_files_exist(self) -> None:
        if not os.path.isdir(MM_PATH):
            os.mkdir(MM_PATH)

        if not os.path.exists(BUCKET_PATH):
            self.write_to_disk(BUCKET_PATH, [])
        if not os.path.exists(ALBUM_PATH):
            self.write_to_disk(ALBUM_PATH, [])

    def read_bucket_list(self) -> None:
        with open(BUCKET_PATH, "r", encoding="utf-8") as bucket_file:
            self.bucket_list = json.load(bucket_file)

    def add_to_bucket_list(self, release_id : int) -> None:
        if release_id not in self.bucket_list:
            self.bucket_list.append(release_id)
            self.write_to_disk(BUCKET_PATH, self.bucket_list)

    def remove_from_bucket_list(self, release_id : int) -> None:
        self.bucket_list.remove(release_id)
        self.write_to_disk(BUCKET_PATH, self.bucket_list)

    def read_album_list(self) -> None:
        with open(ALBUM_PATH, "r", encoding="utf-8") as album_file:
            temp : list = json.load(album_file)
            for t in temp:
                # ** = dictionary unpacking
                # values from temp are mapped to class object
                obj : dict = json.loads(t)
                self.album_list.append(Listened(**obj))

    def add_to_album_list(self, new_entry : Listened) -> None:
        exists : bool = False
        for a in self.album_list:
            if a.release_id == new_entry.release_id:
                exists = True
        if not exists:
            self.album_list.append(new_entry)
            albums_list_serialized : list = list(map(Listened.toJSON, self.album_list))
            self.write_to_disk(ALBUM_PATH, albums_list_serialized)

    def edit_entry_in_album_list(self, edited_entry : Listened) -> None:
        for a in self.album_list:
            if a.release_id == edited_entry.release_id:
                a.rating = edited_entry.rating
                a.thoughts = edited_entry.thoughts
                albums_list_serialized : list = list(map(Listened.toJSON, self.album_list))
                self.write_to_disk(ALBUM_PATH, albums_list_serialized)

    def remove_from_album_list(self, release_id : int) -> None:
        index_to_be_removed : int = 0
        index_found : bool = False
        for i in range(len(self.album_list)):
            if self.album_list[i].release_id == release_id:
                index_to_be_removed = i
                index_found = True
        if index_found:
            self.album_list.pop(index_to_be_removed)
            albums_list_serialized : list = list(map(Listened.toJSON, self.album_list))
            self.write_to_disk(ALBUM_PATH, albums_list_serialized)

    def write_to_disk(self, path : str, array : list) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(array, file)