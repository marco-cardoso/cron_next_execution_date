import datetime

from ..cron import CRON


def get_execution_day_str(current_day: int, exe_day: int) -> str:
    if current_day == exe_day:
        return "today"
    if (current_day + 1) == exe_day:
        return "tomorrow"

    raise ValueError("Package still not configured to work with more than a day of difference")


def get_msg(nxt_cron_exe_date: datetime, exe_day: str, file: str) -> str:
    hr_min = nxt_cron_exe_date.strftime("%H:%M")
    message = f"{hr_min} {exe_day} - {file}"
    return message


def format_output(cron: CRON) -> str:
    current_exe_date = cron.current_date
    nxt_cron_exe_date = cron.next_execution_date

    exe_day = get_execution_day_str(current_exe_date.day, nxt_cron_exe_date.day)
    message = get_msg(nxt_cron_exe_date, exe_day, cron.file)
    return message


def print_output(msg: str):
    print(msg)
