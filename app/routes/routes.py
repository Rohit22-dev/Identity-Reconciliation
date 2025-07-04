from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.crud import create_contact, get_contact_network, get_contacts_by_email_or_phone
from app.core.db import get_db_session
from app.schemas.schemas import IdentifyRequest

router = APIRouter()


@router.post("/identify", response_model=Dict[str, Any])
async def identify_contact( 
    contact_data: IdentifyRequest, db: Session = Depends(get_db_session)
):
    """
    Identify and reconcile contact information
    """
    email = contact_data.email
    phone_number = contact_data.phoneNumber

    if not email and not phone_number:
        raise HTTPException(
            status_code=400, detail="Either email or phoneNumber must be provided"
        )

    # Find existing contacts with the same email or phone
    existing_contacts = get_contacts_by_email_or_phone(db, email, phone_number)

    if not existing_contacts:
        # No existing contacts found, create a new primary contact
        new_contact = create_contact(
            db=db, email=email, phone_number=phone_number, link_precedence="primary"
        )

        response = {
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [new_contact.email] if new_contact.email else [],
                "phoneNumbers": [new_contact.phone_number]
                if new_contact.phone_number
                else [],
                "secondaryContactIds": [],
            }
        }
        return response

    # Get all contacts in the same network
    contact_ids = {c.id for c in existing_contacts}
    network_contacts, _ = get_contact_network(db, contact_ids)

    # Find the primary contact (should be only one after get_contact_network)
    primary_contacts = [c for c in network_contacts if c.link_precedence == "primary"]
    if not primary_contacts:
        # This should not happen if get_contact_network worked correctly
        raise HTTPException(
            status_code=500, detail="No primary contact found in network"
        )

    primary_contact = primary_contacts[0]
    secondary_contacts = [
        c for c in network_contacts if c.link_precedence == "secondary"
    ]

    # Check if we need to create a new secondary contact
    existing_emails = {c.email.lower() for c in network_contacts if c.email}
    existing_phones = {c.phone_number for c in network_contacts if c.phone_number}

    new_email = email and email.lower() not in existing_emails
    new_phone = phone_number and phone_number not in existing_phones

    if new_email or new_phone:
        # Create a new secondary contact
        new_contact = create_contact(
            db=db,
            email=email if new_email else None,
            phone_number=phone_number if new_phone else None,
            linked_id=primary_contact.id,
            link_precedence="secondary",
        )
        secondary_contacts.append(new_contact)

    # Prepare response
    emails = list({c.email for c in [primary_contact] + secondary_contacts if c.email})
    phone_numbers = list(
        {
            c.phone_number
            for c in [primary_contact] + secondary_contacts
            if c.phone_number
        }
    )

    response = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": emails,
            "phoneNumbers": phone_numbers,
            "secondaryContactIds": [c.id for c in secondary_contacts],
        }
    }

    return response 