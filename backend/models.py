import json

class Listened:
    """
    Utility class that represents an album the user has listened to.
    It holds the ID of the album release on Discogs,
    the user's rating from 1-10 and their thoughts on the work.
    """
    
    def __init__(self, release_id, rating, thoughts) -> None:
        self.release_id = release_id
        self.rating = rating
        self.thoughts = thoughts

    def toJSON(self) -> str:
        """Returns this Listened object as a string."""
        return json.dumps(
            self,
            default=lambda o : o.__dict__,
            sort_keys=False,
            indent=4
        )
    
class ProcessedRelease:
    def __init__(self, release_id : int, artists : str, title : str, genres : str, year : int):
        self.release_id = release_id
        self.artists = artists
        self.title = title
        self.genres = genres
        self.year = year

    def __str__(self) -> str:
        return f"{self.release_id}: {self.artists} - {self.title} [{self.genres}] ({self.year})"