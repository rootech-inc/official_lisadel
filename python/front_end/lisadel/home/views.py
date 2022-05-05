from django.core.mail import send_mail
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from . import models
from django.core.exceptions import ObjectDoesNotExist


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
    try:
        event = models.tours.objects.get(url_parse=event)
    except ObjectDoesNotExist:
        return redirect('tours')
    event_uni = event.tour_uni

    # get gallery items
    event_gallery = models.TourGallery.objects.filter(event=event_uni)

    # get packages
    event_packs = models.TourPackage.objects.filter(event=event_uni)

    context = {
        'event': event,
        'events': all_tours,
        'page_title': 'Tourism Events | ' + str(event.title),
        'event_timeline': models.timeline.objects.filter(event=event.tour_uni),
        'event_gallery': event_gallery,
        'event_packs': event_packs
    }
    return render(request, 'home/event.html', context)


# vew gallery
def gallery(request):
    return render(request, 'home/gallery.html')


# book an event
def error_404(request, exception):
    data = {}
    return render(request, 'home/404.html', data)


def book_event(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email_address']
        mobile = request.POST['mobile']
        sits = request.POST['sits']
        package = request.POST['package']
        event = request.POST['event']
        event_name = request.POST['event_name']

        # insert into database
        book = models.EventBooking(
            client_name=full_name,
            email_address=email,
            phone_number=mobile,
            sits=sits,
            booking_package=package,
            event=event
        )

        message = "Client is booking for " + str(sits) + " sit(s). Email: " + str(email) + ", Mobile: " + str(mobile)
        subject = 'Event Booking : ' + str(event_name)
        sender = 'robot'
        recipients = ['rootbackup10@gmail.com']
        if send_mail(subject, message, sender, recipients, fail_silently=False):
            book.save()
            return render(request, 'home/booing_successful.html')
        else:
            return Http404

        return HttpResponse(request)
    else:
        return HttpResponse("Form should be posted")
