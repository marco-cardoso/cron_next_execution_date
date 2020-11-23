import pytest
from ..cron import CRON
from ..utils import time, argument_reader


def test_valid_hour():
    assert time.valid_hour(-2) is False
    assert time.valid_hour(24) is False
    assert time.valid_hour(44) is False
    assert time.valid_hour(4) is True
    assert time.valid_hour(0) is True
    assert time.valid_hour(23) is True


def test_valid_minute():
    assert time.valid_minute(-2) is False
    assert time.valid_minute(67) is False
    assert time.valid_minute(30) is True
    assert time.valid_minute(20) is True


def test_validate_cron_cmd():
    current_time = argument_reader.get_current_datetime("14:00")

    cmd = "* * /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "*       * /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "* *       /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "*"
    assert cron.hour == "*"

    cmd = "35 * /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "35"
    assert cron.hour == "*"

    cmd = "* 5 /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "*"
    assert cron.hour == "5"

    cmd = "5 5 /bin/test.sh"
    cron = CRON(cmd, current_time)
    assert cron.minute == "5"
    assert cron.hour == "5"

    cmd = "95 5 /bin/test.sh"
    with pytest.raises(ValueError):
        CRON(cmd, current_time)

    cmd = "* 25 /bin/test.sh"
    with pytest.raises(ValueError):
        CRON(cmd, current_time)

    cmd = "* -2 /bin/test.sh"
    with pytest.raises(AttributeError):
        CRON(cmd, current_time)

    cmd = "* -2 /"
    with pytest.raises(AttributeError):
        CRON(cmd, current_time)

    # cmd = "* * /dasda@xa@!#^DA "
    # with pytest.raises(ValueError):
    #     CRON(cmd)

    cmd = "*  /dasda@xa@!#^DA "
    with pytest.raises(AttributeError):
        CRON(cmd, current_time)


def test_get_next_cron_datetime():

    cmd = "* * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("14:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 14) and (next_dt.day == current_time.day)

    cmd = "* * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("00:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day)

    cmd = "* 1 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("00:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 1) and (next_dt.day == current_time.day)

    cmd = "* 22 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("00:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 22) and (next_dt.day == current_time.day)

    cmd = "* 19 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("19:43")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 43) and (next_dt.hour == 19) and (next_dt.day == current_time.day)

    cmd = "* 19 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("19:59")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 59) and (next_dt.hour == 19)

    cmd = "* 0 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:59")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day + 1)

    cmd = "* 0 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("00:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day)

    cmd = "0 * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("00:00")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0)

    cmd = "0 * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("19:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 20) and (next_dt.day == current_time.day)

    cmd = "0 * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:30")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day) + 1

    cmd = "5 * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("19:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 5) and (next_dt.hour == 19) and (next_dt.day == current_time.day)

    cmd = "0 * /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day + 1)

    cmd = "0 0 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 0) and (next_dt.day == current_time.day + 1)

    cmd = "5 23 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 5) and (next_dt.hour == 23) and (next_dt.day == current_time.day)

    cmd = "0 23 /bin/test.sh"
    current_time = argument_reader.get_current_datetime("23:01")
    cron = CRON(cmd, current_time)
    next_dt = cron.next_execution_date
    assert (next_dt.minute == 0) and (next_dt.hour == 23) and (next_dt.day == current_time.day + 1)
