from __future__ import absolute_import

import json

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .spotify import song
from .lyrics import fetchLyrics
from .gifextractor import getGIFList


def search(request):
	print("YO")  # TODO Remove.
	query = request.GET['search']
	title, artist, uri = song(query)
	r = getGIFList(title, artist)	
	response = {}
	response['uri'] = uri
	response['gifs'] = []
	for url, duration in r:
		response['gifs'].append({'url': url, 'duration': duration * 1000})
	return HttpResponse(json.dumps(response), content_type='application/json')

def index(request):    
	return render(request, 'index.html', {})