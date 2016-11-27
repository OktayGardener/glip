from __future__ import absolute_import

# Some test with de Giphy API
import sys
import random
import json
import math
import multiprocessing

from .lyrics import fetchLyrics
#from visufy.lyrics import fetchLyrics

if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.request import URLError
    from urllib.parse import quote_plus

else:
    from urllib import urlopen
    from urllib2 import URLError
    from urllib import quote_plus


# TODO what picture to propose if no one is propose by giphy
def getGIF(keyword_list):
    """
    Search gif picture related to a set of keywords
    it will pick a ramdom picture from
    :param keyword_list: list of keywords
    :return: (gifurl, gifkeyword) where gifurl is the url of a related gif URL pick ramdomly from a list of 100 pictures
    which has been given by Giphy.com, and gifkeyword is the word which has been used to seacrh the gif.
    """
    # https://github.com/Giphy/GiphyAPI
    limit = 25
    key = 'dc6zaTOxFJmzC' # public key, subject to rate limit
    # a production can be requested for high usage
    if len(keyword_list) != 0:
        keyword_query = random.choice(keyword_list)
    else:
        keyword_query = "Music"

    formated_keyword_query = quote_plus(keyword_query.encode('utf-8'))
    giphyApiquery = 'http://api.giphy.com/v1/gifs/search?q=' + formated_keyword_query + '&api_key='+key+'&limit=' + str(limit)
    try:
        url = urlopen(giphyApiquery)
        json_res = url.read().decode('utf8')
        data = json.loads(json_res)
        n = len(data['data'])
        if n == 0:
            return []
        rand_idx = random.randint(0, n-1)
        gifurl = data['data'][rand_idx]['images']['downsized']['url']
    except URLError:
        return []

    return [gifurl, keyword_query]



def getRandomGIF():
    # https://github.com/Giphy/GiphyAPI
    limit = 25
    key = 'dc6zaTOxFJmzC'  # public key, subject to rate limit
    # a production can be requested for high usage
    # TODO check for special characters
    # keyword_query = '+'.join(keyword_list)
    giphyApiquery = 'http://api.giphy.com/v1/gifs/random?api_key=' + key
    try:
        url = urlopen(giphyApiquery)
        json_res = url.read().decode('utf8')
        data = json.loads(json_res)
        gifurl = data['data']['image_original_url']
    except URLError:
        return []

    return [gifurl, ""]



#print(getGIF(["day"]))

def getGIFInfo(x):
    artist, keywords, duration, lyrics = x

    gifinfo = getGIF(keywords)
    if len(gifinfo) == 0:
        gifinfo = getGIF([artist])
    if len(gifinfo) == 0:
        gifinfo = getRandomGIF()

    gifurl = gifinfo[0]
    gifkeyword = gifinfo[1]

    return (gifurl, duration, gifkeyword, lyrics)

def getGIFList(artist, song_title):
    """TODO Document."""
    # get the (keyword, duration) list from the lyrics
    l_keyword_duration = fetchLyrics(song_title, artist)

    # if the language is not supported we return an empty list
    if len(l_keyword_duration) == 0:
        return []

    l_gif_duration = []
    for kwd in l_keyword_duration:
        keywords = kwd[0]
        duration = kwd[1]
        lyrics = kwd[2]
        gifinfo = getGIF(keywords)
        if len(gifinfo) == 0:
            gifinfo = getGIF([artist])
        if len(gifinfo) == 0:
            gifinfo = getRandomGIF()

        gifurl = gifinfo[0]
        gifkeyword = gifinfo[1]

        l_gif_duration.append((gifurl, duration, gifkeyword, lyrics))


    return l_gif_duration

def getGIFListMultiprocess(artist, song_title):
        """TODO Document."""
        # get the (keyword, duration) list from the lyrics
        l_keyword_duration = fetotifchLyrics(song_title, artist)

        # if the language is not supported we return an empty list
        if len(l_keyword_duration) == 0:
            return []


        no_cpu = multiprocessing.cpu_count()
        arg = [(artist,) + x for x in l_keyword_duration]
        a = 1
        with multiprocessing.Pool(no_cpu) as p:
           l_total_gif_duration = p.map(getGIFInfo, arg)

        return l_total_gif_duration
