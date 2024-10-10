def send_message(email, message):
    if not email:
        raise ValueError("Email address missing")
    print(f"Sending message to {email}: {message}")