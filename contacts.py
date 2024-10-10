import re
from datetime import datetime

class Contact:
    def __init__(self, name: str, email: str, preferred_time: str):
        # Validate inputs when creating a new contact
        self.name = self.validate_name(name)
        self.email = self.validate_email(email)
        self.preferred_time = self.validate_time(preferred_time)

    def validate_name(self, name: str) -> str:
        """Validates that the name is a non-empty string."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        return name.strip()

    def validate_email(self, email: str) -> str:
        """Validates that the email follows the correct format."""
        # Basic regex for validating email
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise ValueError(f"Invalid email address: {email}")
        return email

    def validate_time(self, time_str: str) -> str:
        """Validates the preferred time format as HH:MM AM/PM."""
        try:
            # Use datetime to check if the time is in the correct format
            valid_time = datetime.strptime(time_str, "%I:%M %p")
            return time_str
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM (24-hour).")
    
    def __repr__(self):
        """Represent the contact with name and email for readability."""
        return f"Contact(name='{self.name}', email='{self.email}', preferred_time='{self.preferred_time}')"

class ContactList:
    def __init__(self) -> None:
        self.contacts = []
    
    def add_contact(self, name: str, email: str, preferred_time = None) -> None:
        if preferred_time == None:
            preferred_time = "08:00 AM"
        
        contact = Contact(name=name, email=email, preferred_time=preferred_time)
        self.contacts.append(contact)
    
    def remove_contact(self, name) -> None:
        self.contacts = [c for c in self.contacts if c.name != name]

    def get_contacts(self) -> list:
        return self.contacts
    
