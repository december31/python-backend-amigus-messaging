from datetime import datetime
import random
import time


def current_time_millis():
    return round(time.time() * 1000)

def random_datetime(start: datetime, end: datetime) -> datetime:
    """
    Generates a random datetime object between two given datetime objects.
    """
    # Convert start and end datetimes to Unix timestamps (float)
    start_timestamp = start.timestamp()
    end_timestamp = end.timestamp()

    # Generate a random timestamp between the start and end
    random_timestamp = random.uniform(start_timestamp, end_timestamp)

    # Convert the random timestamp back to a datetime object
    return datetime.fromtimestamp(random_timestamp)