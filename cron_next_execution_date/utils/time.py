def valid_minute(minute: int) -> bool:
    """
    Validate if the given minute is within the range 0-59
    :param minute: An integer representing the minute
    :return: A boolean representing the validation
    """
    return (minute >= 0) & (minute <= 59)


def valid_hour(hour: int) -> bool:
    """
    Validate if the given hour is within the range 0-23
    :param hour: An integer representing the hour
    :return: A boolean representing the validation
    """
    return (hour >= 0) & (hour <= 23)
