from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True, index=True)
    linked_id = Column(Integer, ForeignKey('contacts.id'), nullable=True, index=True)
    link_precedence = Column(String, nullable=False)  # 'primary' or 'secondary'
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Self-referential relationship
    linked_contact = relationship('Contact', remote_side=[id], backref='secondary_contacts')
