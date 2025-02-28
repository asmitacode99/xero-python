# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    XERO_CLIENT_ID = os.getenv("XERO_CLIENT_ID")
    XERO_CLIENT_SECRET = os.getenv("XERO_CLIENT_SECRET")
    XERO_REDIRECT_URI = os.getenv("XERO_REDIRECT_URI")
    XERO_SCOPE = os.getenv("XERO_SCOPE", "openid profile email accounting.transactions accounting.contacts offline_access")
    XERO_AUTH_URL = "https://login.xero.com/identity/connect/authorize"
    XERO_TOKEN_URL = "https://identity.xero.com/connect/token"
    XERO_TENANT_ID = os.getenv("XERO_TENANT_ID")

settings = Settings()
