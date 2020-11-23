"""
    Module responsible to read and format the current time argument from CLI
"""
from collections import namedtuple
from datetime import datetime
import re
import sys

CURRENT_TIME_RE = "^(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})$"
Time = namedtuple('Time', ['hour', 'minute'])


def get_current_time_str() -> str:
    """
    Get the current time from CLI
    :return: A string with the given time
    :raises ValueError: If the format is not HH:MM
    """
    arg = str(sys.argv[1])
    valid_arg = __validate_current_time_re(arg)
    if valid_arg:
        return arg
    else:
        raise ValueError("Current time must follow the pattern HH:MM ")


def get_current_datetime(time: str) -> datetime:
    """
    Transform a given time string into a datetime object respecting its hour
    and minute
    :param time: A string following the format HH:MM
    :return: A datetime object with the current date and the hour/minute given in the
    time parameter
    """
    dt = datetime.now()
    hour, minute = __get_time_components(time)
    dt = dt.replace(hour=hour, minute=minute)
    return dt


def __validate_current_time_re(time: str) -> bool:
    """
    Apply the below Regular Expression to check whether the given time format
    is valid or not.

    ^(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})$

    :param time: A string following the format HH:MM
    :return: A boolean result with whether the time is valid or not
    """
    valid_re = bool(re.match(CURRENT_TIME_RE, time))
    return valid_re


def __get_time_components(time: str) -> Time:
    """
    Apply the below Regular Expression to split the time into hour and minute.

    ^(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})$

    :param time: A string following the format HH:MM
    :return: A namedtuple with the hour and minute
    """
    match = re.match(CURRENT_TIME_RE, time)

    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    return Time(hour, minute)
