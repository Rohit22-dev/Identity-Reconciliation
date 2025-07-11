from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.models import Contact
from datetime import datetime, timezone
from typing import List, Tuple, Set


def get_contacts_by_email_or_phone(
    db: Session, email: str = None, phone_number: str = None
) -> List[Contact]:
    """
    Retrieve contacts by email or phone number
    Returns all contacts that match either the email or phone number
    """
    if not email and not phone_number:
        return []

    # Create a query with OR condition for email or phone number
    conditions = []
    if email:
        conditions.append(Contact.email == email)
    if phone_number:
        conditions.append(Contact.phone_number == phone_number)

    # Find all contacts that match either condition
    return db.query(Contact).filter(or_(*conditions)).all()


def get_contact_network(
    db: Session, contact_ids: Set[int]
) -> Tuple[List[Contact], Set[int]]:
    """
    Get all contacts in the same network (primary and secondary contacts)
    """
    if not contact_ids:
        return [], set()

    # Keep expanding the network until we don't find any new contacts
    all_network_ids = set(contact_ids)
    previous_count = 0
    
    while len(all_network_ids) > previous_count:
        previous_count = len(all_network_ids)
        
        # Find all contacts that are linked to these IDs or have these as linked_id
        contacts = (
            db.query(Contact)
            .filter((Contact.id.in_(all_network_ids)) | (Contact.linked_id.in_(all_network_ids)))
            .all()
        )
        
        # Add all found contact IDs to the network
        all_network_ids.update({c.id for c in contacts})
        
        # Also add linked_id for any secondary contacts we found
        for contact in contacts:
            if contact.linked_id:
                all_network_ids.add(contact.linked_id)

    # Get all contacts in the final network
    final_contacts = (
        db.query(Contact)
        .filter(Contact.id.in_(all_network_ids))
        .all()
    )

    # Check if we need to expand further (in case of multiple primary contacts that need to be linked)
    primary_contacts = [c for c in final_contacts if c.link_precedence == "primary"]
    if len(primary_contacts) > 1:
        # If we have multiple primary contacts, we need to link them
        primary_contacts.sort(key=lambda x: x.created_at)
        oldest_primary = primary_contacts[0]

        # Update other primary contacts to be secondary
        for contact in primary_contacts[1:]:
            contact.link_precedence = "secondary"
            contact.linked_id = oldest_primary.id
            contact.updated_at = datetime.now(timezone.utc)
            db.add(contact)

        db.commit()

        # Get updated contacts
        return get_contact_network(
            db, {oldest_primary.id} | {c.id for c in primary_contacts[1:]}
        )

    return final_contacts, all_network_ids


def create_contact(
    db: Session,
    email: str = None,
    phone_number: str = None,
    linked_id: int = None,
    link_precedence: str = "primary",
) -> Contact:
    """
    Create a new contact
    """
    contact = Contact(
        email=email,
        phone_number=phone_number,
        linked_id=linked_id,
        link_precedence=link_precedence,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def get_primary_contact(db: Session, contact: Contact) -> Contact:
    """
    Get the primary contact for a given contact
    """
    if contact.link_precedence == "primary":
        return contact
    if contact.linked_id:
        return db.query(Contact).filter(Contact.id == contact.linked_id).first()
    return contact
