import sys
from contacts import ContactList, Contact
from logger import print_logs
from message_generator import message_generator
from message_sender import send_message
from datetime import datetime, timedelta

def check_time_window(input_time_str):
    # Get the current time
    current_time = datetime.now()

    # Format the input time string (e.g., "08:00 AM") and combine it with today's date
    input_time = datetime.strptime(input_time_str, "%I:%M %p")
    input_time = input_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)

    # Calculate 15 minutes before and after the current time
    time_15_min_before = current_time - timedelta(minutes=15)
    time_15_min_after = current_time + timedelta(minutes=15)

    # Check if the input time is within, before, or after the window
    if time_15_min_before <= input_time <= time_15_min_after:
        return (True, "")
    elif input_time < time_15_min_before:
        return (False, "before")
    else:
        return (False, "after")
    
def message_already_sent_today(contact_name: str) -> bool:
    """Check if a message has already been sent to this contact today."""
    today = datetime.now().date()

    try:
        with open("log.txt", "r") as log_file:
            for line in log_file:
                # Split the log line and extract the date and contact name
                log_time_str, log_message = line.split(" - Sent to ")
                log_date = datetime.strptime(log_time_str.strip(), "%Y-%m-%d %H:%M:%S.%f").date()
                
                # Check if the log date is today and the message is for the same contact
                if log_date == today and log_message.startswith(contact_name):
                    return True
    except FileNotFoundError:
        # If the log file doesn't exist, no message has been sent
        return False
    
    return False

def force_send_all(my_contacts: ContactList):
    """Force send messages to all contacts regardless of preferred time."""
    for c in my_contacts.get_contacts():
        msg = message_generator(c)
        send_message(c, msg)

def send_appropriate_messages(my_contacts: ContactList):
    """Send messages only to contacts whose preferred time is within the 15-minute window."""
    for c in my_contacts.get_contacts():
        if not message_already_sent_today(c.name):
            time_check = check_time_window(c.preferred_time)

            if time_check[0]:
                msg = message_generator(c)
                send_message(c, msg)
            elif time_check[1] == "before":
                print(f"Message Not sent: preferred time for {c.name} ({c.preferred_time}) is before the relevant window.")
            elif time_check[1] == "after":
                print(f"Message Not sent: preferred time for {c.name} ({c.preferred_time}) is after the relevant window.")
        else:
            print(f"Message Not sent: already sent to {c.name} today. Skipping...")

def main():
    # Initialize contacts
    my_contacts = ContactList()
    my_contacts.add_contact("Jens", "jens@python.org")
    my_contacts.add_contact("Nils", "nils@goolge.com", "10:30 AM")
    my_contacts.add_contact("Finn", "finn@facebook.com", "11:00 AM")
    my_contacts.add_contact("Knut", "knut@microsoft.com", "06:43 PM")
    
    # Display the current time
    print(f"\nCurrent Time: {datetime.now().strftime('%I:%M %p')}\n")

    # Display options to the user
    print("Choose an option:")
    print("1. Force send messages to all contacts")
    print("2. Send messages to only appropriate contacts (check preferred time)")
    print("3. Print all entries from current and previous days from log.txt")
    print("4. Exit")

    choice = input("\nEnter your choice (1/2/3/4): ")

    if choice == '1':
        print("\nForcing send messages to all contacts...\n")
        force_send_all(my_contacts)

    elif choice == '2':
        print("\nSending messages to appropriate contacts based on their preferred time...\n")
        send_appropriate_messages(my_contacts)

    elif choice == '3':
        print("\nLog entries from today and yesterday:\n")
        print_logs()

    elif choice == '4':
        print("Exiting...")
        sys.exit()

    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__=="__main__":
    main()