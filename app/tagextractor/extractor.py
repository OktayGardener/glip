from PyLyrics import *
from topia.termextract import extract

def getLyrics(artist, song):
    text = PyLyrics.getLyrics(artist, song)
    text = text.split('\n')
    return text

def getTerms(text):
    terms = []
    extractor = extract.TermExtractor()
    extractor.filter = extract.permissiveFilter
    for t in text:
        ext = extractor(t)
        newterms = []
        for e in ext:
            newterms.append(e[0])
        terms.append(newterms)
    return terms

def processSong(artist, song):
    text = getLyrics(artist, song)
    terms = getTerms(text)
    return text, terms
