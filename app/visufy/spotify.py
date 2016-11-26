from spotipy import Spotify

sp = Spotify()


def song(query):
    """Search Spotify and retrieve a relevant song."""
    tracks = sp.search(q=query, type='track')['tracks']['items']
    if tracks:
        # TODO Is it safe to assume that the first result is always the most relevant?
        return tracks[0]['artist'], tracks[0]['title'], tracks[0]['uri']
    else: 
        return 'Cerulean Crayons', 'Compulsive Dreamer', 'spotify:track:1yqYEOKDj2OakM49MKlqvW'
