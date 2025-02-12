from django.urls import path
from . import views

urlpatterns = [
    path("authorize", views.authorize, name="authorize"),
    path("callback", views.callback, name="callback"),
    path("contacts", views.get_contacts, name="contacts"),
]