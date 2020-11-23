from collections import namedtuple
from datetime import datetime
import re
import sys

CURRENT_TIME_RE = "^(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{2})$"
Time = namedtuple('Time', ['hour', 'minute'])


def get_current_time_arg() -> str:
    arg = str(sys.argv[1])
    valid_arg = __validate_current_time_re(arg)
    if valid_arg:
        return arg
    else:
        raise ValueError("Current time must follow %h:%M ")


def get_current_datetime(time: str) -> datetime:
    dt = datetime.now()
    hour, minute = __get_time_components(time)
    dt = dt.replace(hour=hour, minute=minute)
    return dt


def __validate_current_time_re(time: str) -> bool:
    valid_re = bool(re.match(CURRENT_TIME_RE, time))
    return valid_re


def __get_time_components(time: str) -> Time:
    match = re.match(CURRENT_TIME_RE, time)

    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    return Time(hour, minute)
