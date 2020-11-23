import re


def read_cron_cmd():
    try:
        expression = input()
        cron = CRON(expression)
        return cron
    except EOFError:
        return None


def valid_minute(minute: int):
    return (minute >= 0) & (minute <= 59)


def valid_hour(hour: int):
    return (hour >= 0) & (hour <= 23)


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
