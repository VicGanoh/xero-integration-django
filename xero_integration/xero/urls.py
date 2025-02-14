from django.urls import path
from . import views

urlpatterns = [
    path("authorize/", views.authorize, name="authorize"),
    path("callback/", views.callback, name="callback"),
    path("sync_contacts/", views.sync_xero_contacts, name="sync_xero_contacts"),
    path("create_contacts/", views.create_contacts, name="create_contacts"),
]