from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from app.config import settings
from app.auth import get_access_token, TOKEN_STORAGE

def get_xero_client():
    """Initialize the Xero API client with proper configuration."""
    access_token = get_access_token()
    if not access_token:
        raise Exception("Not authenticated. Please login via /auth/login.")

    configuration = Configuration()
    configuration.access_token = access_token
    configuration.host = "https://api.xero.com/api.xro/2.0"  

    client = ApiClient(configuration)
    if client is None:
        raise Exception("Failed to create Xero API Client.")

    return client

def get_xero_accounting_api():
    """Retrieve the Xero Accounting API client with Tenant ID."""
    from xero_python.accounting import AccountingApi

    client = get_xero_client()
    xero_tenant_id = TOKEN_STORAGE.get("xero_tenant_id")  

    if not xero_tenant_id:
        raise Exception("Xero Tenant ID is missing. Please authenticate first.")

    print(f"Using Tenant ID: {xero_tenant_id}")

    accounting_api = AccountingApi(client)
    accounting_api.xero_tenant_id = xero_tenant_id  

    return accounting_api
