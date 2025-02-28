# app/routes/contacts.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.contact import ContactCreate, ContactResponse
from app.dependencies import get_xero_accounting_api
from app.services.xero_service import get_contacts, create_contact
from app.auth import get_access_token

router = APIRouter()

@router.get("/contacts", response_model=list[ContactResponse])
def list_contacts(accounting_api=Depends(get_xero_accounting_api)):
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized. Please login at /auth/login")
    return get_contacts(accounting_api)

@router.post("/contacts", response_model=ContactResponse)
def add_contact(contact: ContactCreate, accounting_api=Depends(get_xero_accounting_api)):
    access_token = get_access_token()
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized. Please login at /auth/login")
    return create_contact(accounting_api, contact)
