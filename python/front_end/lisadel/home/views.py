from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    # return HttpResponse("Hello World")
    return render(request, 'home/index.html')


# view single event
def event_view(request, event):
    return render(request, 'home/event.html')
