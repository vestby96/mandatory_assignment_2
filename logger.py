from datetime import datetime

def log_message(contact, message):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - Sent to {contact.name}: {message}\n")