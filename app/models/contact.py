# app/models/contact.py
from pydantic import BaseModel
from typing import Optional

class ContactBase(BaseModel):
    name: str
    email: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    contact_id: str
