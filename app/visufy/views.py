from django.shortcuts import render
from django.http import HttpResponse
from .forms import SongForm
# Create your views here.

def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SongForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO do werk
            render(request, 'index.html', {'form': form})
        #    return HttpResponseRedirect('/video/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = SongForm()
    return render(request, 'index.html', {'form': form})

def video(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'video.html')
