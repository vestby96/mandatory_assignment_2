# logger.py

from datetime import datetime, timedelta
from morning_greetings.contacts import Contact

def log_message(c: Contact, msg: str):
    with open("log.txt", "a") as f:
        f.write(f"{datetime.now()} - Sent to {c.name} ({c.email}): {msg}\n")

def print_logs():
    """Print log entries from today and the previous day."""
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    try:
        with open("log.txt", "r") as log_file:
            for line in log_file:
                # The log timestamp is the first part of the line (before ' - Sent to ')
                log_time_str = line.split(" - ")[0].strip()
                
                # Convert the timestamp string to a datetime object
                try:
                    log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    # Handle cases where the microseconds might not be included in the log
                    log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S")
                
                # If the log is from today or yesterday, print it
                if log_time.date() in [today.date(), yesterday.date()]:
                    print(line.strip())
    except FileNotFoundError:
        print("Log file not found.")