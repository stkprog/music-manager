from discogs_client import Client
from discogs_client.models import Release, MixedPaginatedList, Master
from backend.models import BucketAlbum
import re

class DiscogsHelper:
    """Utility class for interaction with the Discogs API."""

    def __init__(self, token) -> None:
        self.d : Client = Client("MusicManager/0.1", user_token=token)
    
    def search_one(self, user_query : str) -> BucketAlbum:
        result = ""
        try:
            result = self.d.search(user_query, type="master").page(1)[0]
        except:
            return None
        
        main_release = result.main_release
        artists = []
        for artist in main_release.artists:
            artists.append(self.process_artist(artist.name))
        artists : str = self.array_to_comma_separated_string(artists)
        genres : str = self.array_to_comma_separated_string(main_release.genres)
        year : str = self.process_year(result, main_release)

        return BucketAlbum(main_release.id, artists, main_release.title, genres, year)

    def process_artist(self, artist : str) -> str:
        """
        If an artist name is used by several artists, Discogs appends a
        number at the end, e.g. Queen (2).
        If this is the case, this function removes it.
        """
        regex_result = re.findall(r"[(\d)]", artist)
        if len(regex_result) == 0:
            return artist
        else:
            return artist[:-len(regex_result) - 1]

    def process_year(self, master : Release, main_release : Release) -> str:
        """
        In rare cases, year might be unknown for whatever reason,
        or differ between releases.
        If it can't be found, add string "Unknown"
        """
        year : str = ""
        if main_release.year == 0 and master.year == 0:
            year = "Unknown"
        elif main_release.year > 0 or (main_release.year == 0 and master.year > 0):
            year = str(master.year)
        return year
    
    def array_to_comma_separated_string(self, array : list) -> str:
        """Takes a list and returns it as a comma separated string."""
        comma_separated : str = ""
        if len(array) > 1:
            for i in range(len(array)):
                comma_separated += array[i]
                if i < len(array) - 1:
                    comma_separated += ", "
        elif len(array) == 1:
            comma_separated = array[0]
        return comma_separated