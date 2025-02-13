import logging

from celery import shared_task
from django.conf import settings

from .models import Contact
from .utils import add_address_info, add_contact_person_info, add_phone_info


logger = logging.getLogger(__name__)


@shared_task
def sync_xero_contacts_task(contacts):
    try:
        print("======== Syncing contacts =======")
        settings.SYNC_XERO_SIGNALS = False
        print("================================")
        print("Is Signal On: ", settings.SYNC_XERO_SIGNALS)
        contacts = contacts.get("Contacts")
        for contact in contacts:
            is_contact_supplier = contact.get("IsSupplier")
            is_contact_customer = contact.get("IsCustomer")

            contact_obj, created = Contact.objects.update_or_create(
                xero_contact_id=contact.get("ContactID"),
                defaults={
                    "name": contact.get("Name"),
                    "email": contact.get("EmailAddress", ""),
                    "is_supplier": is_contact_supplier,
                    "is_customer": is_contact_customer,
                },
            )
            add_phone_info(contact, contact_obj)
            add_address_info(contact, contact_obj)
            add_contact_person_info(contact, contact_obj)
    finally:
        settings.SYNC_XERO_SIGNALS = True
        print("================================")
        print("Is Signal On: ", settings.SYNC_XERO_SIGNALS)
