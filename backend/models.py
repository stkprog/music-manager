import json

class Album():
    """A super class representing a simple album."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : int):
        self.release_id = release_id
        self.artists = artists
        self.title = title
        self.genres = genres
        self.year = year

    def toJSON(self) -> str:
        """Returns this object as a JSON string."""
        return json.dumps(
            self,
            default=lambda o : o.__dict__,
            sort_keys=False,
            indent=4
        ) 

class BucketAlbum(Album):
    """Represents a release from the user's bucket list."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : int):
        super(BucketAlbum, self).__init__(release_id, artists, title, genres, year)

class ListenedAlbum(Album):
    """Represents a release the user has listened to."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : int, rating : int, thoughts : str):
        super(ListenedAlbum, self).__init__(release_id, artists, title, genres, year)
        self.rating = rating
        self.thoughts = thoughts