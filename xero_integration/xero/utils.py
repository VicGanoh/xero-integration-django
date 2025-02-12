from xero_integration.xero.models import Contact, ContactAddress, ContactPerson, ContactPhoneNumber
from django_countries import countries


def save_contact_info(contacts: dict):
    """
    Save contact information to the database.

    Args:
        contacts (dict): A dictionary containing contact information.

    Returns:
        None
    """
    contacts = contacts.get("Contacts")
    for contact in contacts:
        is_contact_supplier = contact.get("IsSupplier")
        is_contact_customer = contact.get("IsCustomer")

        contact_obj, created = Contact.objects.update_or_create(
            xero_contact_id=contact.get("ContactID"),
            defaults={
                "name": contact.get("Name"),
                "email": contact.get("EmailAddress", ""),
                "website": contact.get("Website", ""),
                "is_supplier": is_contact_supplier,
                "is_customer": is_contact_customer,
            },
        )

        add_phone_info(contact, contact_obj)
        add_address_info(contact, contact_obj)
        add_contact_person_info(contact, contact_obj)

def add_phone_info(contact, contact_obj):
    """
    Add phone information to a contact object.

    Args:
        contact (dict): The contact information containing phone details.
        contact_obj (Contact): The contact object to which the phone information will be added.

    Returns:
        None
    """
    for phone_info in contact.get("Phones", []):
        phone_number = phone_info.get("PhoneNumber")
        phone_country_code = phone_info.get("PhoneCountryCode")
        phone_area_code = phone_info.get("PhoneAreaCode")

        if phone_number and phone_number != "":
            phone_number_str: str = ""
            if phone_country_code:
                phone_number_str += str(phone_country_code)

            if phone_area_code:
                phone_number_str += str(phone_area_code)

            phone_number_str += str(phone_number)

            contact_phonenumber, created = ContactPhoneNumber.objects.update_or_create(
                company_name=contact_obj,
                phone_label=phone_info.get("PhoneType"),
                defaults={
                    "phone_number": phone_number_str,
                },
            )

def add_address_info(contact: list, contact_obj: Contact):
    """
    Add address information to the contact object.

    Args:
        contact (dict): The contact information.
        contact_obj (Contact): The contact object.

    Returns:
        None
    """
    for address in contact.get("Addresses", []):
        # Create a dictionary of fields that are not empty
        fields: dict = {
            "address_line1": address.get("AddressLine1"),
            "address_line2": address.get("AddressLine2"),
            "address_line3": address.get("AddressLine3"),
            "address_line4": address.get("AddressLine4"),
            "address_type": address.get("AddressType"),
            "city": address.get("City"),
            "region": address.get("Region"),
            "postal_code": address.get("PostalCode"),
            "country": address.get("Country"),
        }

        # Convert country name to country code
        if fields["country"]:
            for code, name in countries:
                if name == fields["country"]:
                    fields["country"] = code
                    break

        fields = {k: v for k, v in fields.items() if v is not None and v != ""}  # Remove empty fields

        if fields:  # If there are any non-empty fields
            contact_address, created = ContactAddress.objects.update_or_create(
                company_name=contact_obj,
                address_type=fields.get("address_type"),
                defaults=fields,
            )


def add_contact_person_info(contact: dict, contact_obj: Contact) -> None:
    # Check if the contact has either FirstName, LastName, or EmailAddress
    first_name = contact.get("FirstName", "")
    last_name = contact.get("LastName", "")
    email = contact.get("EmailAddress", "")

    if first_name or last_name or email:
        # If so, save it as a primary contact person
        ContactPerson.objects.update_or_create(
            company_name=contact_obj,
            defaults={
                "job_title": contact.get("JobTitle", ""),
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "primary_contact": True,
            },
        )

    # Proceed with the original logic for the contact persons
    contact_persons = contact.get("ContactPersons", [])
    existing_contact_persons = ContactPerson.objects.filter(
        company_name=contact_obj,
        job_title__in=[cp.get("JobTitle", "") for cp in contact_persons],
        first_name__in=[cp.get("FirstName", "") for cp in contact_persons],
        last_name__in=[cp.get("LastName", "") for cp in contact_persons],
        email__in=[cp.get("EmailAddress") for cp in contact_persons],
        phone__in=[cp.get("PhoneNumber", "") for cp in contact_persons],
    )

    existing_contact_persons_dict = {cp.email: cp for cp in existing_contact_persons}

    for contact_person in contact_persons:
        email = contact_person.get("EmailAddress")
        if email in existing_contact_persons_dict:
            # Update existing contact person
            existing_cp = existing_contact_persons_dict[email]
            existing_cp.job_title = contact_person.get("JobTitle", "")
            existing_cp.first_name = contact_person.get("FirstName", "")
            existing_cp.last_name = contact_person.get("LastName", "")
            existing_cp.phone = contact_person.get("PhoneNumber", "")
            existing_cp.primary_contact = contact_person.get("PrimaryContact", False)
            existing_cp.save()
        else:
            # Create new contact person
            ContactPerson.objects.create(
                company_name=contact_obj,
                job_title=contact_person.get("JobTitle", ""),
                first_name=contact_person.get("FirstName", ""),
                last_name=contact_person.get("LastName", ""),
                email=email,
                phone=contact_person.get("PhoneNumber", ""),
                primary_contact=contact_person.get("PrimaryContact", False),
            )
