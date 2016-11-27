from spotipy import Spotify

sp = Spotify()


def song(query):
    """Search Spotify and retrieve a relevant song."""
    tracks = sp.search(q=query, type='track')['tracks']['items']
    if tracks:
        # TODO Is it safe to assume that the first result is always the most relevant?

        # Always take first artist only.
        track = tracks[0]
        artist = track['artists'][0]['name']
        title = track['name']
        uri = tracks[0]['uri']
        return artist, title, uri
    else: 
        return 'Cerulean Crayons', 'Compulsive Dreamer', 'spotify:track:1yqYEOKDj2OakM49MKlqvW'
