# app/auth.py
import httpx
from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from app.config import settings

router = APIRouter()

# In-memory token storage (for demo purposes)
TOKEN_STORAGE = {}

@router.get("/login")
def login():
    """Redirect user to Xero’s OAuth2 login page."""
    auth_url = (
        f"{settings.XERO_AUTH_URL}?"
        f"response_type=code&client_id={settings.XERO_CLIENT_ID}"
        f"&redirect_uri={settings.XERO_REDIRECT_URI}"
        f"&scope={settings.XERO_SCOPE}"
    )
    return RedirectResponse(url=auth_url)

    
@router.get("/callback")
async def callback(request: Request):
    """Handle the callback from Xero after user authorization."""
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code not provided."}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.XERO_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.XERO_REDIRECT_URI,
                "client_id": settings.XERO_CLIENT_ID,
                "client_secret": settings.XERO_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    token_data = response.json()
    
    if "access_token" not in token_data:
        return {"error": "Failed to retrieve access token", "details": token_data}
    
    # Get Tenant ID from Xero API
    async with httpx.AsyncClient() as client:
        tenant_response = await client.get(
            "https://api.xero.com/connections",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
    
    tenant_data = tenant_response.json()
    
    if not tenant_data:
        return {"error": "Failed to retrieve tenant ID", "details": tenant_data}
    
    # Save the tokens and tenant ID
    TOKEN_STORAGE["access_token"] = token_data["access_token"]
    TOKEN_STORAGE["refresh_token"] = token_data["refresh_token"]
    TOKEN_STORAGE["expires_in"] = token_data["expires_in"]
    TOKEN_STORAGE["xero_tenant_id"] = tenant_data[0]["tenantId"]  # Store tenant ID

    return {"message": "Authentication successful. You can now access protected endpoints."}

def get_access_token():
    """Utility function to retrieve the stored access token."""
    return TOKEN_STORAGE.get("access_token")
