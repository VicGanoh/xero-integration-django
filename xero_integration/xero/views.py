from functools import wraps
from typing import Any
from django.shortcuts import redirect
from authlib.integrations.django_client import OAuth, DjangoOAuth2App
from django.conf import settings
from requests_oauthlib import OAuth2Session
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.identity import IdentityApi
from xero_python.accounting import AccountingApi
from commons.utils import CustomOAuth2Token
from .tasks import sync_xero_contacts_task
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger(__name__)

api_client = ApiClient(
    Configuration(
        debug=True,
        oauth2_token=CustomOAuth2Token(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET,
        ),
    ),
    pool_threads=1,
)


oauth = OAuth()

oauth2_client = OAuth2Session(
    client_id=settings.CLIENT_ID,
    scope=(
        "offline_access openid profile email accounting.transactions "
        "accounting.contacts accounting.contacts.read"
    ),
    redirect_uri=settings.REDIRECT_URI,
)


oauth.register(
    name="xero",
    version="2",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    endpoint_url="https://api.xero.com/",
    authorize_url="https://login.xero.com/identity/connect/authorize",
    access_token_url="https://identity.xero.com/connect/token",
    refresh_token_url="https://identity.xero.com/connect/token",
    scope= (
        "offline_access openid profile email accounting.transactions "
        "accounting.contacts accounting.contacts.read"
    ),
    jwks_uri="https://identity.xero.com/.well-known/openid-configuration/jwks",
)

xero: DjangoOAuth2App = oauth.xero

@api_client.oauth2_token_getter
def obtain_xero_oauth2_token():
    token = cache.get("token")
    logger.info("Cached token: %s", token)
    if token:
        return token["token"]
    return None


@api_client.oauth2_token_saver
def store_xero_oauth2_token(token):
    # oauth2_token = {
    #     "id_token": token.get("id_token"),
    #     "access_token": token.get("access_token"),
    #     "refresh_token": token.get("refresh_token"),
    #     "token_type": token.get("token_type"),
    #     "expires_in": token.get("expires_in"),
    #     "expires_at": token.get("expires_at"),
    #     "scope": token.get("scope"),
    # }
    store_token = {
        "token": token,
        "modified": True
    }
    cache.set("token", store_token)
    logger.info("Stored token: %s", store_token)

def xero_token_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        xero_token = obtain_xero_oauth2_token()
        logger.info("Xero token required: %s", xero_token)
        if not xero_token:
            return redirect("authorize")

        return function(*args, **kwargs)

    return decorator

def authorize(request):
    if not obtain_xero_oauth2_token():
        redirect_uri = settings.REDIRECT_URI
        response = xero.authorize_redirect(
            request,
            redirect_uri,
            state=settings.STATE
        )
        return response
    return redirect("admin:index")

@csrf_exempt
def callback(request):
    try:
        response = oauth.xero.authorize_access_token(request)
        logger.info("Token response on callback: %s", response)
        if response is None or response.get("access_token") is None:
            return f"Access denied: {response}"
        store_xero_oauth2_token(response)
        return redirect("sync_xero_contacts")
    except Exception as e:
        raise

def get_xero_tenant_id():
    token = obtain_xero_oauth2_token()
    logger.info("Token: %s", token)
    if not token:
        return None

    identity_api: IdentityApi = IdentityApi(api_client)
    logger.info("Identity API: %s", identity_api.api_client)
    for connection in identity_api.get_connections():
        if connection.tenant_type == "ORGANISATION":
            return connection.tenant_id

@xero_token_required
def sync_xero_contacts(request):
    tenant_id = get_xero_tenant_id()
    logger.info("Tenant ID: %s", tenant_id)
    accounting_api = AccountingApi(api_client)
    contacts = accounting_api.get_contacts(xero_tenant_id=tenant_id)
    contacts = serialize(contacts)
    sync_xero_contacts_task.apply_async(args=[contacts])
    return redirect("admin:index")

@xero_token_required
def create_contacts(request):
    tenant_id = get_xero_tenant_id()
    contact_data: list[dict[str, Any]] = []
    contact_data.append({
        "contact_id": "1234567890",
        "name": "John Doe",
        "email_address": "john.doe@example.com",
        "is_supplier": True,
        "is_customer": False,
    })
    accounting_api = AccountingApi(api_client)
    try:
        result = accounting_api.create_contacts(
            xero_tenant_id=tenant_id,
            contacts=contact_data,
            summarize_errors=False
        )
        logger.info("Result: %s", result)
    except Exception as e:
        logger.error("Error: %s", e)
    return redirect("admin:index")