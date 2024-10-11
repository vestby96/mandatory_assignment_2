from datetime import datetime
from contacts import Contact

def message_generator(c: Contact):
    # Parse the preferred time string (e.g., "08:00 AM")
    time = datetime.strptime(c.preferred_time, "%I:%M %p")
    
    # Extract the hour to determine the time of day
    hour = time.hour

    # Generate message based on the time of day
    if 5 <= hour < 12:  # Morning (5 AM - 12 PM)
        return f"Good morning {c.name}, hope you have a great day!"
    elif 12 <= hour < 18:  # Afternoon (12 PM - 6 PM)
        return f"Good afternoon {c.name}, hope you're having a productive day!"
    else:  # Evening (6 PM - 5 AM)
        return f"Good evening {c.name}, hope you're winding down and relaxing!"