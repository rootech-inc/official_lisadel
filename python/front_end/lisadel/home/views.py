from django.http import HttpResponse
from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    # return HttpResponse("Hello World")
    all_tours = models.tours.objects.all()[:6]
    services = models.services.objects.all()
    gallery = models.TourGallery.objects.all()[:10]

    context = {
        'events': all_tours,
        'page_title': 'Home',
        'services': services,
        'gallery': gallery
    }
    return render(request, 'home/index.html', context)


# about us
def about_us(request):
    context = {
        'page_title': 'About Us',
        'team_member': models.team.objects.all()
    }
    return render(request, 'home/about-us.html', context)


# services
def services(request):
    context = {
        'page_title': 'Services',
        'all_services': models.services.objects.all()
    }
    return render(request, 'home/services.html', context)


# service
def service(request, service):
    srv = models.services.objects.get(url_parse=service)
    context = {
        'page_title': 'Services | ' + str(srv.title),
        'service': srv,
        'all_services': models.services.objects.all().exclude(url_parse=service)
    }
    return render(request, 'home/service.html', context)


# events
def events(request):
    all_tours = models.tours.objects.all()[:12]

    context = {
        'events': all_tours,
        'page_title': 'Tourism Events',
    }
    return render(request, 'home/events.html', context)


# view single event
def event_view(request, event):
    all_tours = models.tours.objects.all()[:12]
    event = models.tours.objects.get(url_parse=event)
    event_uni = event.tour_uni

    # get gallery items
    event_gallery = models.TourGallery.objects.filter(event=event_uni)

    context = {
        'event': event,
        'events': all_tours,
        'page_title': 'Tourism Events | ' + str(event.title),
        'event_timeline': models.timeline.objects.filter(event=event.tour_uni),
        'event_gallery':event_gallery
    }
    return render(request, 'home/event.html', context)


def gallery(request):
    return render(request, 'home/gallery.html')
