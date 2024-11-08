import discogs_client
d = discogs_client.Client("MusicManager/0.1", user_token="WtnXidDMzVdRoJfDNRRRZaMvWlznSylYLFENKbkm")

def search(user_query : str):
    results = d.search(user_query)
    print(results[0])