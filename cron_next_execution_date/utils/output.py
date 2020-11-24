"""
    Module responsible to format the output message
"""
import datetime

from cron import CRON


def get_execution_day_str(current_day: int, exe_day: int) -> str:
    """
    Get if the execution date is today or tomorrow
    :param current_day: An integer representing the current day
    :param exe_day: An integer representing the CRON execution day
    :return: 'today' or 'tomorrow' as string
    """
    if current_day == exe_day:
        return "today"
    if (current_day + 1) == exe_day:
        return "tomorrow"

    raise ValueError("Package still not configured to work with more than a day of difference")


def format_msg(nxt_cron_exe_date: datetime, exe_day: str, file: str) -> str:
    """
    Responsible to format the output message
    :param nxt_cron_exe_date: A datetime object representing the next execution date
    :param exe_day: A datetime object representing the execution day - Today or Tomorrow
    :param file: A string with the script to be executed
    :return: A string with the formatted message
    """
    hr_min = nxt_cron_exe_date.strftime("%H:%M")
    message = f"{hr_min} {exe_day} - {file}"
    return message


def get_output(cron: CRON) -> str:
    """
    Get the output message from a CRON object
    :param cron: A cron object
    :return: A string with the output message
    """
    current_exe_date = cron.current_date
    nxt_cron_exe_date = cron.next_execution_date

    exe_day = get_execution_day_str(current_exe_date.day, nxt_cron_exe_date.day)
    message = format_msg(nxt_cron_exe_date, exe_day, cron.file)
    return message


def print_output(msg: str):
    """
    Responsible to output the message
    :param msg: String with the message
    """
    print(msg)
