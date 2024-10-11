from contacts import Contact
from logger import log_message

def send_message(c: Contact, msg: str):
    if not c.email:
        raise ValueError("Email address missing")
    print(f"Sending message to {c.email}: {msg}")
    log_message(c, msg)