from __future__ import absolute_import

import json

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .spotify import song
from .spotify import searchsongs
from .lyrics import fetchLyrics
from .gifextractor import getGIFList


def search(request):
	query = request.GET['search']
	artist, title, uri = song(query)
	print(artist + " - " + title)
	r = getGIFList(artist, title)
	response = {}
	response['uri'] = uri
	response['artist'] = artist
	response['title'] = title
	response['gifs'] = []
	for url, duration, keyword, lyrics in r:
		response['gifs'].append({'url': url, 'duration': duration * 1000, 'keyword': keyword, 'lyrics': lyrics})
	return HttpResponse(json.dumps(response), content_type='application/json')


def autocomp(request):
	query = request.GET['search']
	songs = searchsongs(query)
	response = {}
	response['songs'] = []
	for artist, title, uri in songs:
		response['songs'].append({'label': artist + " - " + title, 'value': uri})
	return HttpResponse(json.dumps(response), content_type='application/json')

def index(request):
	return render(request, 'index.html', {})
