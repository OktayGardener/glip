from spotipy import Spotify

sp = Spotify()


def song_uri(query):
    """Search Spotify and retrieve the URI to the most relevant song."""
    tracks = sp.search(q=query, type='track')['tracks']['items']
    if tracks:
        # TODO Is it safe to assume that the first result is always the most relevant?
        return tracks[0]['uri']
    else: 
        return 'spotify:track:1yqYEOKDj2OakM49MKlqvW'


# TODO Refactor tests into own package?
def test_song_url():

	# Search for something.
	assert song_url("Cerulean Crayons") == 'spotify:track:1yqYEOKDj2OakM49MKlqvW'
	
	# Search for something that should not exist, pick the default song.
	assert song_url("qv8qn083nq03nv0q3nv0qnc08nq03vnas") == 'spotify:track:1yqYEOKDj2OakM49MKlqvW'
