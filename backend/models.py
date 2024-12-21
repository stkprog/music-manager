import json

class Album():
    """A super class representing a simple album."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : str):
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
    
    def return_self_as_tuple(self):
        """
        Returns this album as a tuple in the following format:
        ([YEAR, ARTISTS, TITLE, GENRES], RELEASE_ID)
        """
        return ([self.year, self.artists, self.title, self.genres], self.release_id)

class BucketAlbum(Album):
    """Represents a release from the user's bucket list."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : str):
        super(BucketAlbum, self).__init__(release_id, artists, title, genres, year)

class ListenedAlbum(Album):
    """Represents a release the user has listened to."""
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : str, rating : str, thoughts : str):
        super(ListenedAlbum, self).__init__(release_id, artists, title, genres, year)
        self.rating = rating
        self.thoughts = thoughts
    
    def return_self_as_tuple(self):
        """
        Returns this album as a tuple in the following format:
        ([YEAR, ARTISTS, TITLE, GENRES, RATING, THOUGHTS], RELEASE_ID)
        """
        return ([self.year, self.artists, self.title, self.genres, self.rating, self.thoughts], self.release_id)