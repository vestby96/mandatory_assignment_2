from morning_greetings.contacts import ContactList, Contact
from morning_greetings.logger import print_logs
from morning_greetings.message_generator import message_generator
from morning_greetings.message_sender import send_message
from datetime import datetime, timedelta


def send_message_to_contact(contact: Contact):
    """Sends a message to a contact if not already sent today."""
    if not message_already_sent_today(contact):
        msg = message_generator(contact)
        send_message(contact, msg)
        print(f"Message sent to {contact.name} at {datetime.now()}.")
    else:
        print(f"Message already sent to {contact.name} today. Skipping...")

def message_already_sent_today(contact: Contact) -> bool:
    """Check if a message has already been sent to this contact today, using the email."""
    today = datetime.now().date()

    try:
        with open("log.txt", "r") as log_file:
            for line in log_file:
                # Example log line: "2024-10-03 08:45:12 - Sent to Jens (jens@python.org): Good Morning, Jens!"
                log_time_str, log_details = line.split(" - Sent to ")
                log_date = datetime.strptime(log_time_str.strip(), "%Y-%m-%d %H:%M:%S.%f").date()

                # Extract the email from the log entry (log format: "Name (email)")
                start_email_idx = log_details.find("(") + 1
                end_email_idx = log_details.find(")")
                log_email = log_details[start_email_idx:end_email_idx]

                # Check if the log date is today and the email matches
                if log_date == today and log_email == contact.email:
                    return True
    except FileNotFoundError:
        # If the log file doesn't exist, no message has been sent
        return False
    
    return False


# CRUD Functions for Managing Contacts

def add_contact(my_contacts: ContactList):
    """Add a new contact."""
    name = input("Enter contact's name: ").strip()
    email = input("Enter contact's email: ").strip()
    preferred_time = input("Enter preferred time (e.g., 08:00 AM): ").strip()

    if preferred_time == "":
        my_contacts.add_contact(name, email)
    else:
        my_contacts.add_contact(name, email, preferred_time)
    print(f"Contact '{name}' added successfully.")


def view_contacts(my_contacts: ContactList):
    """Display all contacts."""
    contacts = my_contacts.get_contacts()
    if not contacts:
        print("No contacts available.")
    else:
        print("\nList of Contacts:")
        for idx, contact in enumerate(contacts, start=1):
            print(f"{idx}. Name: {contact.name}, Email: {contact.email}, Preferred Time: {contact.preferred_time}")


def update_contact(my_contacts: ContactList):
    """Update an existing contact, using either the email or name to find the contact."""
    
    search_key = input("\nEnter the contact's name or email to update: ").strip()

    # Try to find contact by email first (since email is unique)
    matching_contacts = [c for c in my_contacts.get_contacts() if c.email == search_key]

    # If no contact is found by email, try to find by name (there could be multiple)
    if not matching_contacts:
        matching_contacts = [c for c in my_contacts.get_contacts() if c.name.lower() == search_key.lower()]

    # If no contacts are found at all, return an error
    if not matching_contacts:
        print(f"No contact found with name or email '{search_key}'.")
        return

    # If multiple contacts are found by name, let the user choose one
    if len(matching_contacts) > 1:
        print("\nMultiple contacts found with the same name:")
        for idx, contact in enumerate(matching_contacts, start=1):
            print(f"{idx}. Name: {contact.name}, Email: {contact.email}, Preferred Time: {contact.preferred_time}")
        
        try:
            choice = int(input("\nEnter the number of the contact you want to update: ").strip())
            contact = matching_contacts[choice - 1]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return
    else:
        # If only one contact is found, proceed with updating that contact
        contact = matching_contacts[0]

    # Proceed to update the selected contact
    print(f"\nUpdating contact: {contact.name} ({contact.email})")

    # Ask for new email and preferred time, with an option to leave it unchanged
    new_email = input(f"Enter new email (leave blank to keep '{contact.email}'): ").strip()
    new_time = input(f"Enter new preferred time (leave blank to keep '{contact.preferred_time}'): ").strip()

    if new_email:
        contact.email = new_email
    if new_time:
        contact.preferred_time = new_time

    print(f"Contact '{contact.name}' updated successfully.")


def delete_contact(my_contacts):
    """Delete a contact."""
    view_contacts(my_contacts)  # Show current contacts first
    name = input("\nEnter the name of the contact you want to delete: ").strip()

    if my_contacts.remove_contact(name):
        print(f"Contact '{name}' deleted successfully.")
    else:
        print(f"No contact found with the name '{name}'.")


def force_send_all(my_contacts: ContactList):
    """Force send messages to all contacts regardless of preferred time."""
    for c in my_contacts.get_contacts():
        if not message_already_sent_today(c.name):
            msg = message_generator(c.name)
            send_message(c.email, msg)
        else:
            print(f"Message already sent to {c.name} today. Skipping...")


def send_appropriate_messages(my_contacts: ContactList):
    """Send messages only to contacts whose preferred time is within the 15-minute window."""
    for c in my_contacts.get_contacts():
        if not message_already_sent_today(c):
            time_check = check_time_window(c)

            if time_check[0]:
                msg = message_generator(c)
                send_message(c, msg)
            elif time_check[1] == "before":
                print(f"Preferred time for {c.name} ({c.preferred_time}) is before the relevant window.")
            elif time_check[1] == "after":
                print(f"Preferred time for {c.name} ({c.preferred_time}) is after the relevant window.")
        else:
            print(f"Message already sent to {c.name} today. Skipping...")


def check_time_window(c: Contact):
    """Check if the current time is within 15 minutes of the input time."""
    current_time = datetime.now()
    input_time = datetime.strptime(c.preferred_time, "%I:%M %p")
    input_time = input_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)

    time_15_min_before = current_time - timedelta(minutes=15)
    time_15_min_after = current_time + timedelta(minutes=15)

    if time_15_min_before <= input_time <= time_15_min_after:
        return (True, "")
    elif input_time < time_15_min_before:
        return (False, "before")
    else:
        return (False, "after")


def main():
    # Initialize contacts
    my_contacts = ContactList()
    my_contacts.add_contact("Jens", "jens@python.org")
    my_contacts.add_contact("Nils", "nils@goolge.com", "10:30 AM")
    my_contacts.add_contact("Knut", "knut@microsoft.com", "06:43 PM")
    
    while True:
        # Display the current time
        print(f"\nCurrent Time: {datetime.now().strftime('%I:%M %p')}\n")

        # Display options to the user
        print("Choose an option:")
        print("1. Force send messages to all contacts")
        print("2. Send messages to only appropriate contacts (check preferred time)")
        print("3. Add a new contact")
        print("4. View all contacts")
        print("5. Update a contact")
        print("6. Delete a contact")
        print("7. Print all entries from current and previous days from log.txt")
        print("8. Exit")

        choice = input("\nEnter your choice (1/2/3/4/5/6/7/8): ")

        if choice == '1':
            print("\nForcing send messages to all contacts...\n")
            force_send_all(my_contacts)

        elif choice == '2':
            print("\nSending messages to appropriate contacts based on their preferred time...\n")
            send_appropriate_messages(my_contacts)

        elif choice == '3':
            add_contact(my_contacts)

        elif choice == '4':
            view_contacts(my_contacts)

        elif choice == '5':
            update_contact(my_contacts)

        elif choice == '6':
            delete_contact(my_contacts)

        elif choice == '7':
            print("\nLog entries from today and yesterday:\n")
            print_logs()

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
