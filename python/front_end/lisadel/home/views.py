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


# service booking
def service_booking(request):
    if request.method == "POST":
        # get form details
        form = request.POST
        full_name = form['full_name']
        email = form['email']
        phone = form['phone']
        message = form['message']
        service_x = form['service']

        email_message = "<strong>Client</strong> : " + str(full_name) + " <br>" \
                                                                        "<strong>Phone</strong>  : " + str(
            phone) + " <br>" \
                     "<strong>Email</strong>  : " + str(email) + " <br> " \
                                                                 "<strong>Message</strong>  : " + str(message) + " "

        contact = models.contact_us(client_name=full_name, phone_number=phone, email_address=email, message=message)

        subject = 'Service Consultation : ' + service_x
        sender = 'robot'
        recipients = ['rootbackup10@gmail.com']
        if send_mail(subject, email_message, sender, recipients, html_message=email_message, fail_silently=False):
            contact.save()
            return render(request, 'home/booing_successful.html')
        else:
            return Http404

        return HttpResponse(email_message)
    else:
        pass
        # invalid form


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


def visa_consultation(request):
    return render(request, 'home/visa_consultation.html')


## visa booking
def visa_bokk(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        country = request.POST['country']
        city = request.POST['city']
        email = request.POST['email']
        phone = request.POST['phone']
        visa_type = request.POST['visa_type']

        # insert into database
        book = models.EventBooking(
            client_name=full_name,
            email_address=email,
            phone_number=phone,
            sits=1,
            booking_package=visa_type,
            event='visa_booking',
            country=country,
            city=city
        )

        message = "<style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style>" \
                  "<table style='border: 1px solid black;border-collapse: collapse;'>" \
                  "<tr>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>Full Name</th>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>Email Address</th>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>Phone Number<th>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>Country</th>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>City</th>" \
                  "<th style='border: 1px solid black;border-collapse: collapse;'>Visa Type</th>" \
                  "</tr>" \
                  "<tr>" \
                  "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(full_name) + "</td>" \
                                                                                                       "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(
            email) + "</td>" \
                     "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(phone) + "<td>" \
                                                                                                      "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(
            country) + "</td>" \
                       "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(city) + "</td>" \
                                                                                                       "<td style='border: 1px solid black;border-collapse: collapse;'>" + str(
            visa_type) + "</td>" \
                         "</tr>" \
                         "</tr>" \
                         "</table>"
        subject = 'Visa Consultation : ' + visa_type
        sender = 'robot'
        recipients = ['rootbackup10@gmail.com']
        if send_mail(subject, message, sender, recipients, html_message=message, fail_silently=False):
            book.save()
            return render(request, 'home/booing_successful.html')
        else:
            return Http404

        return HttpResponse(request)
    else:
        return HttpResponse("Form should be posted")
