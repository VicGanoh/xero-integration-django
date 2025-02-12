import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


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
