# app/services/xero_service.py
from xero_python.accounting.models import Contact, Contacts
from app.auth import TOKEN_STORAGE
from app.models.contact import ContactCreate
from app.config import settings

def get_contacts(accounting_api):
    """Retrieve contacts from Xero API."""
    xero_tenant_id = TOKEN_STORAGE.get("xero_tenant_id")  # Get tenant ID

    if not xero_tenant_id:
        raise ValueError("Xero Tenant ID is missing. Please authenticate first.")

    print(f"Fetching contacts with Tenant ID: {xero_tenant_id}")  # Debugging

    response = accounting_api.get_contacts(xero_tenant_id=xero_tenant_id)  # ✅ Pass tenant ID
    return response.contacts if response.contacts else []


def create_contact(accounting_api, contact: ContactCreate):
    """Create a new contact in Xero."""
    new_contact = Contact(name=contact.name, email_address=contact.email)
    contacts_payload = Contacts(contacts=[new_contact])
    response = accounting_api.create_contacts(xero_tenant_id=settings.XERO_TENANT_ID, contacts=contacts_payload)
    return response.contacts[0]
