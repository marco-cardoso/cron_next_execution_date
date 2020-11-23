import re
from datetime import datetime, timedelta

from .utils.time import valid_hour, valid_minute


class CRON:
    CRON_RE = "((?P<minute>([0-9]{1,2}|\*))[ ]{1,}(?P<hour>([0-9]{1,2}|\*))[ ]{1,}(?P<file>(\/[A-Za-z0-9._-]+){1,}))"

    def __init__(self, expression: str) -> None:
        super().__init__()

        regex = re.match(self.CRON_RE, expression)

        if regex is None:
            raise AttributeError("Invalid CRON syntax")

        self.minute = str(regex.group("minute"))
        self.hour = str(regex.group("hour"))
        self.file = str(regex.group("file"))

        if (self.minute != '*') and not valid_minute(int(self.minute)):
            raise ValueError("Invalid value. The minute must within the range 0-59")

        if (self.hour != '*') and not valid_hour(int(self.hour)):
            raise ValueError("Invalid value. The minute must within the range 0-23")

    def get_next_execution_date(self, current_datetime: datetime) -> datetime:

        if (self.minute == "*") and (self.hour == "*"):
            next_execution_date = current_datetime + timedelta(minutes=1)
            return next_execution_date
        elif self.minute == "*":
            if int(self.hour) == current_datetime.hour:

                if current_datetime.minute < 59:
                    next_execution_date = current_datetime + timedelta(minutes=1)
                    return next_execution_date
                else:
                    next_execution_date = current_datetime.replace(minute=0) + timedelta(days=1)
                    return next_execution_date

            elif int(self.hour) < current_datetime.hour:
                next_execution_date = current_datetime.replace(hour=int(self.hour), minute=0) + timedelta(days=1)
                return next_execution_date
            elif int(self.hour) > current_datetime.hour:
                next_execution_date = current_datetime.replace(hour=int(self.hour), minute=0)
                return next_execution_date

        elif self.hour == "*":
            if int(self.minute) == current_datetime.minute:
                next_execution_date = current_datetime + timedelta(hours=1)
                return next_execution_date
            elif int(self.minute) < current_datetime.minute:
                next_execution_date = current_datetime.replace(minute=int(self.minute)) + timedelta(hours=1)
                return next_execution_date
            elif int(self.minute) > current_datetime.minute:
                next_execution_date = current_datetime.replace(minute=int(self.minute))
                return next_execution_date
        else:
            next_execution_date = current_datetime.replace(hour=int(self.hour), minute=int(self.minute))

            if next_execution_date > current_datetime:
                return next_execution_date
            else:
                next_execution_date += timedelta(days=1)
                return next_execution_date
