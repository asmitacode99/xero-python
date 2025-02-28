# app/services/xero_service.py
from xero_python.accounting.models import Contact, Contacts
from app.models.contact import ContactCreate
from app.config import settings

def get_contacts(accounting_api):
    """Fetch and return contacts from Xero."""
    response = accounting_api.get_contacts(xero_tenant_id=settings.XERO_TENANT_ID)
    return response.contacts

def create_contact(accounting_api, contact: ContactCreate):
    """Create a new contact in Xero."""
    new_contact = Contact(name=contact.name, email_address=contact.email)
    contacts_payload = Contacts(contacts=[new_contact])
    response = accounting_api.create_contacts(xero_tenant_id=settings.XERO_TENANT_ID, contacts=contacts_payload)
    return response.contacts[0]
