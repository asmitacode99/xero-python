# app/dependencies.py
from xero_python.api_client import ApiClient
from xero_python.api_client.configuration import Configuration
from app.config import settings
from app.auth import get_access_token

def get_xero_client():
    access_token = get_access_token()
    if not access_token:
        raise Exception("Not authenticated. Please login via /auth/login.")
    configuration = Configuration()
    configuration.access_token = access_token
    return ApiClient(configuration)
    
def get_xero_accounting_api():
    from xero_python.accounting import AccountingApi
    client = get_xero_client()
    return AccountingApi(client)
