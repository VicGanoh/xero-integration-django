import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

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

    company_name = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(
        _("Address Type"), max_length=20, choices=AddressTypes.choices, default=AddressTypes.POBOX
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