def valid_minute(minute: int):
    return (minute >= 0) & (minute <= 59)


def valid_hour(hour: int):
    return (hour >= 0) & (hour <= 23)
