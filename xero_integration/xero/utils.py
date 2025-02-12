from xero_python.api_client.oauth2 import OAuth2Token

from xero_integration.xero.validators import validate_possible_phonenumber
from phonenumber_field.modelfields import PhoneNumberField

class CustomOAuth2Token(OAuth2Token):
    def update_token(
        self,
        access_token,
        scope,
        expires_in,
        token_type,
        expires_at=None,
        refresh_token=None,
        id_token=None,
        userinfo=None,
    ):
        """
        Set new auth2 token details
        :param access_token: str
        :param refresh_token: str (optional)
        :param scope: list of strings
        :param expires_at: float timestamp (optioanl)
        :param expires_in: number
        :param token_type: str
        :param id_token: str (optional)
        """
        self.access_token = access_token
        self.expires_at = expires_at
        self.expires_in = expires_in
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.scope = scope
        self.token_type = token_type
        self.userinfo = userinfo


class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_phonenumber]