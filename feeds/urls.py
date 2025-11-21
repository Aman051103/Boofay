from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="feeds"),
    path("about-us/", views.about, name="about"),
    path("contact-us/", views.contact, name="contact"),
    path("sending-query/", views.send_contact, name="sending-query"),
]
