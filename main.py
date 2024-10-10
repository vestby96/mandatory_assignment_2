from contacts import ContactList
from logger import log_message
from message_generator import message_generator
from message_sender import send_message

def main():
    my_contacts = ContactList()
    my_contacts.add_contact("Jens", "jens@python.org")
    my_contacts.add_contact("Nils", "nils@goolge.com", "10:30 AM")
    my_contacts.add_contact("Knut", "knut@microsoft.com", "06:43 PM")

    for c in my_contacts.get_contacts():
        
        msg = message_generator(c.name)
        send_message(c.email, msg)
        log_message(c, msg)

if __name__=="__main__":
    main()