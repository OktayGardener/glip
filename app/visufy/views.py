from __future__ import absolute_import

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .spotify import song
from .lyrics import fetchLyrics
from .gifextractor import getGIFList

def index(request):
    #if request.method == 'POST':
	#	title, artist, uri = song(form.query)
	#	r = getGIFList(title, artist)
	#	print(r)
		# TODO return json string of r
    #else:  # HTTP GET
	return render(request, 'index.html', {})
