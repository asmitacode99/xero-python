# app/routes/contacts.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.contact import ContactCreate, ContactResponse
from app.dependencies import get_xero_accounting_api
from app.services.xero_service import get_contacts, create_contact
from app.auth import get_access_token

router = APIRouter()

def verify_access_token():
    """Helper function to check for valid access token."""
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized. Please login at /auth/login")
    return access_token

@router.get("/contacts", response_model=list[ContactResponse])
def list_contacts(accounting_api=Depends(get_xero_accounting_api)):
    """Fetch and list all contacts from Xero."""
    verify_access_token()  # Ensure the user is authorized
    try:
        return get_contacts(accounting_api)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching contacts: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/contacts", response_model=ContactResponse)
def add_contact(contact: ContactCreate, accounting_api=Depends(get_xero_accounting_api)):
    """Add a new contact to Xero."""
    verify_access_token()  # Ensure the user is authorized
    try:
        return create_contact(accounting_api, contact)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Error creating contact: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
 