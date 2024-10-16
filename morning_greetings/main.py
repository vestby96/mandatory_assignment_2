# main.py

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
                log_time_str, log_details = line.split(" - Sent to ")
                log_date = datetime.strptime(log_time_str.strip(), "%Y-%m-%d %H:%M:%S.%f").date()

                # Extract the email from the log entry (log format: "Name (email)")
                start_email_idx = log_details.find("(") + 1
                end_email_idx = log_details.find(")")
                log_email = log_details[start_email_idx:end_email_idx]

                if log_date == today and log_email == contact.email:
                    return True
    except FileNotFoundError:
        return False
    
    return False

# CRUD Functions for Managing Contacts

def add_contact(my_contacts: ContactList):
    """Add a new contact with error handling."""
    try:
        name = input("Enter contact's name: ").strip()
        email = input("Enter contact's email: ").strip()
        preferred_time = input("Enter preferred time (e.g., 08:00 AM): ").strip()

        if preferred_time == "":
            my_contacts.add_contact(name, email)
        else:
            my_contacts.add_contact(name, email, preferred_time)

        print(f"Contact '{name}' added successfully.")
    except ValueError as e:
        print(f"Error adding contact: {e}. Please try again.")

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
    try:
        search_key = input("\nEnter the contact's name or email to update: ").strip()

        matching_contacts = [c for c in my_contacts.get_contacts() if c.email == search_key]

        if not matching_contacts:
            matching_contacts = [c for c in my_contacts.get_contacts() if c.name.lower() == search_key.lower()]

        if not matching_contacts:
            print(f"No contact found with name or email '{search_key}'.")
            return

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
            contact = matching_contacts[0]

        print(f"\nUpdating contact: {contact.name} ({contact.email})")
        new_email = input(f"Enter new email (leave blank to keep '{contact.email}'): ").strip()
        new_time = input(f"Enter new preferred time (leave blank to keep '{contact.preferred_time}'): ").strip()

        if new_email:
            contact.email = new_email
        if new_time:
            contact.preferred_time = new_time

        print(f"Contact '{contact.name}' updated successfully.")
    except ValueError as e:
        print(f"Error updating contact: {e}. Please try again.")

def delete_contact(my_contacts: ContactList):
    """Delete a contact with error handling."""
    try:
        view_contacts(my_contacts)
        name = input("\nEnter the name of the contact you want to delete: ").strip()

        if my_contacts.remove_contact(name):
            print(f"Contact '{name}' deleted successfully.")
        else:
            print(f"No contact found with the name '{name}'.")
    except ValueError as e:
        print(f"Error deleting contact: {e}. Please try again.")

# Send messages

def force_send_all(my_contacts: ContactList):
    """Force send messages to all contacts regardless of preferred time."""
    for c in my_contacts.get_contacts():
        if not message_already_sent_today(c):
            msg = message_generator(c)
            send_message(c, msg)
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

    print(f"\nCurrent Time: {datetime.now().strftime('%I:%M %p')}\n")
    
    while True:
        print("---------------------------------------------------------------------")
        print("Choose an option:")
        print("1. Force send messages to all contacts")
        print("2. Send messages to only appropriate contacts (check preferred time)")
        print("3. View all contacts")
        print("4. Add a new contact")
        print("5. Update a contact")
        print("6. Delete a contact")
        print("7. Print logs from current and previous days")
        print("8. Exit")

        choice = input("\nEnter your choice (1/2/3/4/5/6/7/8): ")

        try:
            if choice == '1':
                print("\nForcing send messages to all contacts...\n")
                force_send_all(my_contacts)

            elif choice == '2':
                print("\nSending messages to appropriate contacts based on their preferred time...\n")
                send_appropriate_messages(my_contacts)

            elif choice == '3':
                view_contacts(my_contacts)

            elif choice == '4':
                add_contact(my_contacts)

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
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")


if __name__ == "__main__":
    main()