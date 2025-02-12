from django.contrib import admin
from .models import Contact, ContactAddress, ContactPhoneNumber, ContactPerson

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    search_fields = ["name", "email"]
    list_display = ["name", "email", "is_supplier", "is_customer"]
    list_filter = ["is_supplier", "is_customer"]

@admin.register(ContactAddress)
class ContactAddressAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company_name"]
    list_display = ["company_name", "address_type", "city", "country"]
    list_filter = ["address_type", "country"]
    search_fields = ["company_name__name", "city", "address_line1"]

@admin.register(ContactPhoneNumber)
class ContactPhoneNumberAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company_name"]
    list_display = ["company_name", "phone_label", "phone_number"]
    list_filter = ["phone_label"]
    search_fields = ["company_name__name", "phone_number"]

@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company_name"]
    list_display = ["full_name", "company_name", "job_title", "email", "primary_contact"]
    list_filter = ["primary_contact"]
    search_fields = ["first_name", "last_name", "company_name__name", "email"]
