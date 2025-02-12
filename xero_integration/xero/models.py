import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from commons.utils import PossiblePhoneNumberField

class Contact(models.Model):
    """
    Contact is same as the organisation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    xero_contact_id = models.CharField(
        _("Xero Contact ID"),
        max_length=255,
        blank=True,
        default="",
        help_text="Xero Contact ID",
    )
    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text="Name of organization",
        unique=True,
    )
    email = models.EmailField(
        _("Email"),
        max_length=254,
        blank=True,
        default="",
        help_text="Email address of the organization",
    )
    description = models.TextField(_("Description"), blank=True, default="")
    do_not_call = models.BooleanField(default=False)
    linkedin_url = models.URLField(_("Linked in URL"), blank=True, null=True)
    facebook_url = models.URLField(_("Facebook URL"), blank=True, null=True)
    twitter_username = models.CharField(_("Twitter username"), max_length=255, null=True, blank=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    is_supplier = models.BooleanField(_("supplier"), default=False)
    is_customer = models.BooleanField(_("customer"), default=False)

    def __str__(self) -> str:
        return str(self.name)


class ContactAddress(models.Model):
    class AddressTypes(models.TextChoices):
        POBOX = "POBOX", _("P.O. Box")
        POSTAL = "POSTAL", _("Postal")
        RESIDENTIAL = "RESIDENTIAL", _("Residential")
        STREET = "STREET", _("Street")
        DELIVERY = "DELIVERY", _("Delivery")
        DIGITAL_ADDRESS = "DIGITAL ADDRESS", _("Digital Address")

    company_name = models.ForeignKey(
        Contact,
        verbose_name=_("Contact/Company/Organisation"),
        on_delete=models.CASCADE,
        related_name="contact_addresses",
    )
    address_type = models.CharField(
        _("Address Type"),
        max_length=20,
        choices=AddressTypes.choices,
        default=AddressTypes.POBOX,
    )
    address_line1 = models.CharField(
        _("Address Line 1"),
        max_length=256,
        blank=True,
        default="",
    )
    address_line2 = models.CharField(
        _("Address Line 2"),
        max_length=256,
        blank=True,
        default="",
    )
    address_line3 = models.CharField(
        _("Address Line 3"),
        max_length=256,
        blank=True,
        default="",
    )
    address_line4 = models.CharField(
        _("Address Line 4"),
        max_length=256,
        blank=True,
        default="",
    )
    city = models.CharField(
        _("City"),
        max_length=256,
        blank=True,
        default="",
    )
    region = models.CharField(
        _("Region"),
        max_length=128,
        blank=True,
        default="",
        help_text="Region",
    )
    country = CountryField(
        verbose_name=_("country"),
        blank_label="(select country)",
        blank=True,
        null=True,
        max_length=256,
    )
    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
        blank=True,
        default="",
        help_text="Postal code",
    )
    digital_address = models.CharField(
        _("Digital Address"),
        max_length=20,
        blank=True,
        default="",
        help_text="Digital Address",
    )

    class Meta:
        ordering = ("pk",)
        verbose_name = _("Address")
        verbose_name_plural = _("Address")


class ContactPhoneNumber(models.Model):
    class PhoneLabel(models.TextChoices):
        DEFAULT = "DEFAULT", _("Default")
        PERSONAL = "PERSONAL", _("Personal")
        HOME = "HOME", _("Home")
        MOBILE = "MOBILE", _("Mobile")
        FAX = "FAX", _("Fax")
        DDI = "DDI", _("Direct Dial In")

    company_name = models.ForeignKey(
        Contact,
        verbose_name=_("Contact/Company/Organisation"),
        on_delete=models.CASCADE,
        related_name="contact_phonenumbers",
    )
    phone_label = models.CharField(
        _("Phone Label"), max_length=8, choices=PhoneLabel.choices, default=PhoneLabel.MOBILE
    )
    phone_number = PossiblePhoneNumberField(_("Phone number"))

    class Meta:
        verbose_name = _("Phone number")
        verbose_name_plural = _("Phone numbers")
        ordering = ("phone_label", "phone_number")

    def __str__(self) -> str:
        return f"{self.phone_label}: {self.phone_number}"


class ContactPerson(models.Model):
    company_name = models.ForeignKey(
        Contact,
        verbose_name=_("Contact/Company/Organisation"),
        on_delete=models.CASCADE,
        related_name="primary_contact_people",
    )
    job_title = models.CharField(_("Job title"), max_length=254, blank=True, default="")
    first_name = models.CharField(_("First name"), max_length=254)
    last_name = models.CharField(_("Last name"), max_length=254)
    email = models.EmailField(_("Email"), max_length=254, blank=True, null=True, default="")
    phone = PossiblePhoneNumberField(_("Phone number"), null=True)
    primary_contact = models.BooleanField(_("Primary contact"), default=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return f"{str(self.full_name)} {self.company_name.name}"

    class Meta:
        verbose_name = _("Contact Person")
        verbose_name_plural = _("Contact Persons")

    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        super().save(*args, **kwargs)

