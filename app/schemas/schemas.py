from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ContactBase(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
    linked_id: Optional[int] = None
    link_precedence: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class IdentifyResponse(BaseModel):
    contact: dict = {
        "primaryContactId": int,
        "emails": List[str],
        "phoneNumbers": List[str],
        "secondaryContactIds": List[int]
    }
