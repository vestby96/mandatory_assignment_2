# Mandatory Assignment 2
Repo for the 2nd mandatory assignment of Problem Sovling with Scripting

The Morning Greetings package is designed to manage a list of contacts and send personalized messages based on each contact's preferred time. The components include contacts management, message generation, sending mechanisms, and logging. 

Challenges faced:
- Time window validation: Accurately determening whether the current time falls within a 30 minute window of a contact's preferred time. The solution was to let the user choose whether to send all messages without considerring preferred time, or only send messages to those contact's that would prefer a message when the program is run. 
- User input validation: Preventing invalid data, such as incorrect email or time format. The solution included utilizing regex, to check if the inputs follow a certain pattern. 
- Managing duplicate contacts: Handling multiple contacts with the same name or email posed challenges in read, update, and delete operations. The solution was to make emails distict and not allow duplicate emails, and use the email as a way to search for specific users. 

# How to install
1. Download the repo, and navigate to the directory
2. Run the pollowing commands
    - $ pip install .
    - $ pip install --upgrade .

# How to use
After installing the package, run the following command to run the program:
    - $ morning_greetings
Follow the commands presented to complete your desired tasks. 