from backend import discogs
from backend import files

def initialize():
    token = open("token.txt", "r").read()
    discogs.create_discogs_client(token)

def enter():
    discogs.search(input())
    # files.ensure_files_exist()