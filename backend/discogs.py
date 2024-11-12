from discogs_client import Client
from discogs_client.models import Release, MixedPaginatedList

class DiscogsHelper:
    """Utility class for interaction with the Discogs API."""

    def __init__(self, token) -> None:
        self.d : Client = Client("MusicManager/0.1", user_token=token)

    def search(self, user_query : str) -> MixedPaginatedList:
        """Search for the main release of albums using the text provided by the user."""
        results : list = self.d.search(user_query, type="master")
        artists : str = ""

        # Searching for "master releases" instead of "releases"
        # and then getting the main release for this album.
        # For the sake of this program, multiple releases of the same album
        # e.g. in different formats (LP, CD, ...) don't need to be shown to the user.
        for r in results:                       # r = Master
            main_r : Release = r.main_release   # main_r = Release
            artists = self.artists_array_to_comma_separated_string(main_r.artists)
            print(f"{main_r.id}: {artists} - {main_r.title} {main_r.genres}", sep=",")

    def get_release(self, release_id : int) -> Release:
        """Return the main release of the given master album."""
        return self.d.master(release_id).main_release

    def artists_array_to_comma_separated_string(self, array : list) -> str:
        """Takes an array of Discogs artists and returns it as a comma separated list."""
        artists : str = ""
        for i in range(len(array)):
            artists += array[i].name
            if len(array) > 1 and i < len(array) - 1:
                artists += ", "
        return artists