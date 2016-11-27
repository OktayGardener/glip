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
        else:
            track = sp.track("spotify:track:6JEK0CvvjDjjMUBFoXShNZ")
    artist = track['artists'][0]['name']
    title = track['name']
    uri = track['uri']
    return artist, title, uri


def searchsongs(query):
    tracks = sp.search(q=query, type='track', limit=5)['tracks']['items']
    r_tracks = []
    for track in tracks:
        r_tracks.append((track['artists'][0]['name'], track['name'], track['uri']))
    return r_tracks
