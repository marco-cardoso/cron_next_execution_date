import re
from datetime import datetime, timedelta

from utils.time import valid_hour, valid_minute


class CRON:
    """
        Class responsible to convert a CRON expression, separate the execution hour/minute/file
        and calculate the next execution date.
    """

    # This regular expression has 3 groups : minute, hour and file.
    # The minute argument can only be an asterisk or a value inside the range 0-59.
    # The hour argument can only be an asterisk or a value inside the range 0-23.
    # The file argument can only be a string representing a path for a specific file
    #
    # A few CRON expression examples are described as follows :
    # * * /bin/script.sh
    # * 9 /bin/script.sh
    # 2 9 /bin/script.sh
    #
    CRON_RE = "((?P<minute>([0-9]{1,2}|\*))[ ]{1,}(?P<hour>([0-9]{1,2}|\*))[ ]{1,}(?P<file>(\/[A-Za-z0-9._-]+){1,}))"

    def __init__(self, expression: str, current_datetime: datetime = datetime.now()) -> None:
        """

        Apply the regular expression stored in the CRON_RE class variable to validate the CRON command and separate the
        terms.

         At the end of the constructor execution it calculates the next CRON execution date based on
         the parameter current_datetime

        :param expression: A string representing the CRON expression
        :param current_datetime: A datetime object representing the current time
        :raises ValueError: If any of the CRON expression terms are invalid
        """
        super().__init__()

        regex = re.match(self.CRON_RE, expression)

        if regex is None:
            raise ValueError("Invalid CRON syntax")

        self.minute = str(regex.group("minute"))
        self.hour = str(regex.group("hour"))
        self.file = str(regex.group("file"))

        if (self.minute != '*') and not valid_minute(int(self.minute)):
            raise ValueError("Invalid value. The minute must be within the range 0-59")

        if (self.hour != '*') and not valid_hour(int(self.hour)):
            raise ValueError("Invalid value. The minute must be within the range 0-23")

        self.current_date = current_datetime
        self.next_execution_date = self.__get_next_execution_date(current_datetime)

    def __get_next_execution_date(self, current_datetime: datetime) -> datetime:
        """
        Get the CRON next execution date based on the parameter current_datetime
        :param current_datetime: A datetime object representing the current_datetime
        :return: A datetime object representing the next execution date
        """

        if (self.minute == "*") and (self.hour == "*"):
            #
            # The first case is when the CRON is scheduled to execute every minute.
            # As the exercises describes : In the case when the task should fire at
            # the simulated 'current time' then that is the time you should output,
            # not the next one.
            #
            return current_datetime
        elif self.minute == "*":
            #
            # Case when CRON is scheduled to execute every minute of a specific hour
            #
            if int(self.hour) == current_datetime.hour:
                # When the task should fire at the simulated 'current time'
                return current_datetime
            elif int(self.hour) < current_datetime.hour:
                # If the CRON expression hour is smaller than the current hour then
                # it means that the task will only be executed on the next day
                next_execution_date = current_datetime.replace(hour=int(self.hour), minute=0) + timedelta(days=1)
                return next_execution_date
            elif int(self.hour) > current_datetime.hour:
                # If the CRON expression hour is bigger than the current hour then
                # the execution time is on the same day
                next_execution_date = current_datetime.replace(hour=int(self.hour), minute=0)
                return next_execution_date

        elif self.hour == "*":
            #
            # Case when CRON is scheduled to execute every hour at the specific given minute
            #
            if int(self.minute) == current_datetime.minute:
                # When the task should fire at the simulated 'current time'
                return current_datetime
            elif int(self.minute) < current_datetime.minute:
                # If the CRON expression minute is smaller than the current minute time then
                # the execution time is at the next hour
                next_execution_date = current_datetime.replace(minute=int(self.minute)) + timedelta(hours=1)
                return next_execution_date
            elif int(self.minute) > current_datetime.minute:
                # If the CRON expression minute is smaller than the current minute time then
                # the execution time is at the same hour
                next_execution_date = current_datetime.replace(minute=int(self.minute))
                return next_execution_date
        else:
            #
            # Case when CRON is scheduled to execute at a specific minute/hour
            #

            # Replace the current datetime object with the CRON expression hour and minute
            next_execution_date = current_datetime.replace(hour=int(self.hour), minute=int(self.minute))

            if next_execution_date > current_datetime:
                return next_execution_date
            else:
                next_execution_date += timedelta(days=1)
                return next_execution_date


