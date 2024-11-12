from backend.discogs import DiscogsHelper
from backend.files import FileWriter
from backend.models import Listened

def get_token() -> str:
    """Reads and returns the Discogs API personal access token from the specified file."""
    return open("token.txt", "r").read()

def enter() -> None:
    """Entrypoint for the main loop of the program."""
    file_writer = FileWriter()

    discogs_helper = DiscogsHelper(get_token())
    # master_release = discogs_helper.get_release(3643167)
    discogs_helper.search(input())

    # file_writer.ensure_files_exist()
    # file_writer.read_album_list()
    # file_writer.remove_from_album_list(123)
    # file_writer.remove_from_album_list(235346546)