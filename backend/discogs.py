from discogs_client import Client
from discogs_client.models import Release, MixedPaginatedList

class DiscogsHelper:
    def __init__(self, token) -> None:
        self.d : Client = Client("MusicManager/0.1", user_token=token)

    # instead of searching for "releases", searching for "master releases"
    # and then using the main_release property
    # for the sake of this program, multiple releases of the same album
    # e.g. in different formats (lp, cd, ...) don't need to be shown
    def search(self, user_query : str) -> MixedPaginatedList: # ?
        results : list = self.d.search(user_query, type="master")
        artists : str = ""

        for r in results:               # r = Master
            main_r = r.main_release     # main_r = Release
            artists = self.artists_array_to_comma_separated_string(main_r.artists)
            print(f"{main_r.id}: {artists} - {main_r.title} {main_r.genres}", sep=",")

    def get_release(self, release_id : int) -> Release:
        # this on its own only outputs something like
        # <Release 32182818 'Mg Ultra'>
        # return d.release(release_id)
        return self.d.master(release_id).main_release

    def artists_array_to_comma_separated_string(self, array : list) -> str:
        artists : str = ""
        for i in range(len(array)):
            artists += array[i].name
            if len(array) > 1 and i < len(array) - 1:
                artists += ", "
        return artists