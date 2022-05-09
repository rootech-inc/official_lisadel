"""lisadel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='landing'),

    path('tours', views.events, name='tours'),
    path('tour/<event>', views.event_view, name='view_event'),
    path('book-event', views.book_event, name='book_event'),

    path('services', views.services, name='services'),
    path('services/<service>', views.service, name='service'),
    path('service-consultation', views.service_booking, name='service_consultation'),

    path('visa-consultation', views.visa_consultation, name='visa_consultation'),
    path('visa-book', views.visa_bokk, name='visa_bokk'),

    path('about-us', views.about_us, name='about_us'),
    path('gallery', views.gallery, name='gallery'),
]
