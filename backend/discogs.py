from discogs_client import Client
from discogs_client.models import Release, MixedPaginatedList, Master
from backend.models import BucketAlbum
import re

class DiscogsHelper:
    """Utility class for interaction with the Discogs API."""

    def __init__(self, token) -> None:
        self.d : Client = Client("MusicManager/0.1", user_token=token)

    def search_multiple(self, user_query : str) -> list[BucketAlbum]:
        """Search for the main release of albums using the text provided by the user."""
        results : MixedPaginatedList = self.d.search(user_query, type="master").page(1)[0:10]
        artists : str = ""
        processed_results : list[BucketAlbum] = []

        # Searching for "master releases" instead of "releases"
        # and then the main release. multiple releases of the same album
        # e.g. in different formats (LP, CD, ...) don't need to be shown to the user.
        for r in results:                       # r = Master
            main_r : Release = r.main_release   # main_r = Release
            artists = []
            for a in main_r.artists:
                artists.append(self.process_artist(a.name))
            artists = self.array_to_comma_separated_string(artists)
            genres = self.array_to_comma_separated_string(main_r.genres)
            year : int | str = self.process_year(r, main_r)

            processed_results.append(BucketAlbum(
                main_r.id, artists, main_r.title, genres, year
            ))
        return processed_results
    
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
        regex_result = re.findall("[(\d)]", artist)
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

    def get_release(self, release_id : int) -> Release:
        """Return the main release of the given master album."""
        return self.d.master(release_id).main_release

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