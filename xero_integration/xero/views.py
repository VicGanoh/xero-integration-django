from django.shortcuts import render
from authlib.integrations.django_client import OAuth
from django.conf import settings
from requests_oauthlib import OAuth2Session
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token

oauth = OAuth()
xero = oauth.remote_app(
    version="2",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    endpoint_url="https://api.xero.com/",
    authorization_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope= (
        "offline_access openid profile email accounting.transactions "
        "accounting.contacts accounting.contacts.read"
    ),
)

# configure xero-python sdk client
api_client = ApiClient(
    Configuration(
        debug=settings.DEBUG,
        oauth2_token=OAuth2Token(
            client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET
        ),
    ),
    pool_threads=1,
)
