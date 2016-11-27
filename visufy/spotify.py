from spotipy import Spotify

sp = Spotify()

def song(query):
    """If the query is an uri or url, get it instead"""
    if query.startswith("spotify:track:") or query.startswith("https://open.spotify.com/track/"):
        track = sp.track(query)
    else:
        """Search Spotify and retrieve a relevant song."""
        tracks = sp.search(q=query, type='track')['tracks']['items']
        if tracks:
            track = tracks[0]
    artist = track['artists'][0]['name']
    title = track['name']
    uri = track['uri']
    return artist, title, uri
