import uuid


def generate_unique_id():
    # Generate a 5-character unique id
    return str(uuid.uuid4())[:5]


def event_not_found_error():
    raise ValueError('Event not found')


def slot_not_available_error():
    raise ValueError('There is already an event in this slot')


def date_lower_than_today_error():
    raise ValueError('Date cannot be lower than today')


def reminder_not_found_error():
    raise ValueError('Reminder not found')