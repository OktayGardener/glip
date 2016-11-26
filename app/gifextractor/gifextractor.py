# Some test with de Giphy API
import sys
import random
import json
if sys.version_info[0] == 3:
    from urllib.request import urlopen
    from urllib.request import URLError
else:
    from urllib import urlopen
    from urllib import URLError



# TODO what picture to propose if no one is propose by giphy
def getGIF(keyword_list):
    """
    Search gif picture related to a set of keywords
    it will pick a ramdom picture from
    :param keyword_list: list of keywords
    :return: a related gif URL pick ramdomly from a list of 100 pictures
    which has been given by Giphy.com,
    """
    # https://github.com/Giphy/GiphyAPI
    limit = 100
    key = 'dc6zaTOxFJmzC' # public key, subject to rate limit
    # a production can be requested for high usage
    # TODO check for special characters
    keyword_query = '+'.join(keyword_list)
    giphyApiquery = 'http://api.giphy.com/v1/gifs/search?q=' + keyword_query + '&api_key='+key+'&limit=' + str(limit)
    try:
        url = urlopen(giphyApiquery)
        json_res = url.read().decode('utf8')
        data = json.loads(json_res)
        n = len(data['data'])
        if n == 0:
            return ""
        rand_idx = random.randint(0, n-1)
        gifurl = data['data'][rand_idx]['images']['original']['url']
    except URLError:
        gifurl = ""

    return gifurl


#print(getGIF(["ABBA", "london"]))
