import json
import requests

from whoosh.analysis import StemmingAnalyzer, RegexTokenizer, StemFilter, LowercaseFilter, StopFilter

API_LYRICS_URL = "http://api.vagalume.com.br/search.php"
API_TIMING_URL = "http://app2.vagalume.com.br/ajax/subtitle-get.php?action=getBestSubtitle"
API_KEY = ""

stop_words = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]

#this code is not mine! i shamelessly copied it from http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
#all credits go to alko and arturomp @ stack overflow.
#basically, it's a big find/replace.

import re
cList = {
  "ain't": "am not",
  "aren't": "are not",
  "can't": "cannot",
  "can't've": "cannot have",
  "'cause": "because",
  "could've": "could have",
  "couldn't": "could not",
  "couldn't've": "could not have",
  "didn't": "did not",
  "doesn't": "does not",
  "don't": "do not",
  "hadn't": "had not",
  "hadn't've": "had not have",
  "hasn't": "has not",
  "haven't": "have not",
  "he'd": "he would",
  "he'd've": "he would have",
  "he'll": "he will",
  "he'll've": "he will have",
  "he's": "he is",
  "how'd": "how did",
  "how'd'y": "how do you",
  "how'll": "how will",
  "how's": "how is",
  "I'd": "I would",
  "I'd've": "I would have",
  "I'll": "I will",
  "I'll've": "I will have",
  "I'm": "I am",
  "I've": "I have",
  "isn't": "is not",
  "it'd": "it had",
  "it'd've": "it would have",
  "it'll": "it will",
  "it'll've": "it will have",
  "it's": "it is",
  "let's": "let us",
  "ma'am": "madam",
  "mayn't": "may not",
  "might've": "might have",
  "mightn't": "might not",
  "mightn't've": "might not have",
  "must've": "must have",
  "mustn't": "must not",
  "mustn't've": "must not have",
  "needn't": "need not",
  "needn't've": "need not have",
  "o'clock": "of the clock",
  "oughtn't": "ought not",
  "oughtn't've": "ought not have",
  "shan't": "shall not",
  "sha'n't": "shall not",
  "shan't've": "shall not have",
  "she'd": "she would",
  "she'd've": "she would have",
  "she'll": "she will",
  "she'll've": "she will have",
  "she's": "she is",
  "should've": "should have",
  "shouldn't": "should not",
  "shouldn't've": "should not have",
  "so've": "so have",
  "so's": "so is",
  "that'd": "that would",
  "that'd've": "that would have",
  "that's": "that is",
  "there'd": "there had",
  "there'd've": "there would have",
  "there's": "there is",
  "they'd": "they would",
  "they'd've": "they would have",
  "they'll": "they will",
  "they'll've": "they will have",
  "they're": "they are",
  "they've": "they have",
  "to've": "to have",
  "wasn't": "was not",
  "we'd": "we had",
  "we'd've": "we would have",
  "we'll": "we will",
  "we'll've": "we will have",
  "we're": "we are",
  "we've": "we have",
  "weren't": "were not",
  "what'll": "what will",
  "what'll've": "what will have",
  "what're": "what are",
  "what's": "what is",
  "what've": "what have",
  "when's": "when is",
  "when've": "when have",
  "where'd": "where did",
  "where's": "where is",
  "where've": "where have",
  "who'll": "who will",
  "who'll've": "who will have",
  "who's": "who is",
  "who've": "who have",
  "why's": "why is",
  "why've": "why have",
  "will've": "will have",
  "won't": "will not",
  "won't've": "will not have",
  "would've": "would have",
  "wouldn't": "would not",
  "wouldn't've": "would not have",
  "y'all": "you all",
  "y'alls": "you alls",
  "y'all'd": "you all would",
  "y'all'd've": "you all would have",
  "y'all're": "you all are",
  "y'all've": "you all have",
  "you'd": "you had",
  "you'd've": "you would have",
  "you'll": "you you will",
  "you'll've": "you you will have",
  "you're": "you are",
  "you've": "you have"
}

c_re = re.compile('(%s)' % '|'.join(cList.keys()))

def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]
    return c_re.sub(replace, text)

def fetchLyrics(title, artist):
    #TODO Document.
  url = "{}?art={}&mus={}&apikey={}".format(API_LYRICS_URL, artist.encode('utf8'), title.encode('utf8'), API_KEY)
  results = requests.get(url).json()

  # searches for the song, returns empty list if not
  if results["type"] != "exact" and results["type"] != "aprox":
    # print("Can't find lyrics.")
    return []

  song = results["mus"][0]

  # fetches the timing info
  url = "{}&pointerID=${}".format(API_TIMING_URL, song["id"])
  results = requests.get(url).json()

  if type(results) is list:
    # print("Could not find timing")
    return []

  # finds the id for english
  lang_id = -1
  for lang in results["langs"]:
    # print(lang)
    if lang["langAbbr"] == "ENG":
      lang_id = lang["langID"]
      break

  # if not english, return empty list
  if lang_id == -1:
    return []

  # first in list should be empty until song starts
  list_of_keywords = []
  for subs in results["subtitles"]:
    if subs["lID"] == lang_id:
      for text in subs["text_compressed"]:
        start_time = float(text[1])
        duration = start_time
        previous_end_time = start_time
        keywords = []
        keywords.append(title)
        keywords.append(artist)
        list_of_keywords.append( (keywords, duration, "") ) # first keyword is empty, until someone starts to sing
        break

  # fills the keyword list with keywords
  for subs in results["subtitles"]:
    if subs["lID"] == lang_id:
      for text in subs["text_compressed"]:

        songtext = text[0]
        # print(songtext)

        start_time = float(text[1])
        end_time = float(text[2])
        duration = end_time - previous_end_time
        previous_end_time = end_time

        my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter(stoplist=stop_words)
        keywords = [token.text for token in my_analyzer(expandContractions(songtext))]

        keywords = list(set(keywords)) # remove duplicates

        if len(keywords) == 0:
          keywords.append(title.enocde())
          keywords.append(artist.encode())

        list_of_keywords.append( (keywords, duration, songtext) )

    print list_of_keywords
  return list_of_keywords
