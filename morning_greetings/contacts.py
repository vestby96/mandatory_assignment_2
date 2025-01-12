# contacts.py

import re
from datetime import datetime

class Contact:
    def __init__(self, name: str, email: str, preferred_time: str = "08:00 AM"):
        """Initiates the Contact class with name, email, and preferred_time."""
        self.name = self.validate_name(name)
        self.email = self.validate_email(email)
        self.preferred_time = self.validate_time(preferred_time)

    def validate_name(self, name: str) -> str:
        """Validates that name is a non-empty string."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        return name.strip()

    def validate_email(self, email: str) -> str:
        """Validates that email follows the correct format."""
        # Basic regex for validating email format
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email address: {email}")
        return email

    def validate_time(self, time_str: str) -> str:
        """Validates that preferred_time format as HH:MM AM/PM."""
        try:
            # Use datetime to check if the time is in the correct format
            valid_time = datetime.strptime(time_str, "%I:%M %p")
            return time_str
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM AM/PM (12-hour).")
    
    def __repr__(self):
        """Represent the contact with name and email for readability."""
        return f"Contact(name='{self.name}', email='{self.email}', preferred_time='{self.preferred_time}')"

class ContactList:
    def __init__(self) -> None:
        """Initiates the ContactList class."""
        self.contacts = []
    
    def add_contact(self, name: str, email: str, preferred_time: str = "08:00 AM") -> None:
        """Creates and appends a new contact with name, email, and preferred_time."""
        if any(c.email == email for c in self.contacts):
            raise ValueError(f"Contact with email ({email}) already exists.")
        
        contact = Contact(name=name, email=email, preferred_time=preferred_time)
        self.contacts.append(contact)
    
    def remove_contact(self, email: str = None, name: str = None) -> bool:
        """Removes a contact by email or name and returns True if a contact was removed, False otherwise."""
        initial_length = len(self.get_contacts())
        if email:
            self.contacts = [c for c in self.get_contacts() if c.email != email]
        elif name:
            self.contacts = [c for c in self.get_contacts() if c.name != name]
        return len(self.contacts) < initial_length

    def update_contact(self, email: str, name: str = None, preferred_time: str = None) -> bool:
        """Update an existing contact's name or preferred time."""
        c = self.find_contact_by_email(email)
        if name:
            c.name = c.validate_email(name)
        if preferred_time:
            c.preferred_time = c.validate_time(preferred_time)
        return True

    def get_contacts(self) -> list[Contact]:
        """Returns list of all contacts."""
        return self.contacts
    
    def find_contact_by_email(self, email: str) -> Contact:
        """Find a contact by email."""
        for c in self.get_contacts():
            if c.email == email:
                return c
        raise ValueError(f"Contact with email ({email}) not found.")
    
    def find_contact_by_name(self, name: str) -> list[Contact]:
        """Find all contacts with name."""
        contacts = []

        for c in self.get_contacts():
            if c.name == name:
                contacts.append(c)
        
        if len(contacts) == 0:
            raise ValueError(f"Contact with name ({name}) not found.")
        
        return contacts

    def __repr__(self) -> str:
        """Represent the contact list with length and names for readability."""
        return f"ContactList({len(self.contacts)} contacts: {', '.join([c.name for c in self.contacts])})"