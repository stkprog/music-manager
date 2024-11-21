from discogs_client import Client
from discogs_client.models import Release, MixedPaginatedList
from backend.models import ProcessedRelease

class DiscogsHelper:
    """Utility class for interaction with the Discogs API."""

    def __init__(self, token) -> None:
        self.d : Client = Client("MusicManager/0.1", user_token=token)

    def search(self, user_query : str) -> MixedPaginatedList:
        """Search for the main release of albums using the text provided by the user."""
        results : MixedPaginatedList = self.d.search(user_query, type="master").page(1)[0:10]
        artists : str = ""
        processed_results : list[ProcessedRelease] = []

        # Searching for "master releases" instead of "releases"
        # and then getting the main release for this album.
        # For the sake of this program, multiple releases of the same album
        # e.g. in different formats (LP, CD, ...) don't need to be shown to the user.
        for r in results:                       # r = Master
            main_r : Release = r.main_release   # main_r = Release
            artists = self.array_to_comma_separated_string(
                list(map(lambda x : x.name, main_r.artists))
            )
            genres = self.array_to_comma_separated_string(main_r.genres)

            year : int | str = self.process_year(r, main_r)

            processed_results.append(ProcessedRelease(
                main_r.id, artists, main_r.title, genres, year
            ))
        return processed_results

    def process_year(self, master : Release, main_release : Release) -> int | str:
        """
        In rare cases, year might be unknown for whatever reason,
        or differ between releases.
        If it can't be found, add string "Unknown"
        """
        year : int | str = 0
        if main_release.year == 0 and master.year == 0:
            year = "Unknown"
        elif main_release.year > 0 or (main_release.year == 0 and master.year > 0):
            year = master.year
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