import discogs_client

def create_discogs_client(token):
    global d
    d = discogs_client.Client("MusicManager/0.1", user_token=token)

def search(user_query : str):
    results = d.search(user_query, type="release")
    print(results[0].genres)